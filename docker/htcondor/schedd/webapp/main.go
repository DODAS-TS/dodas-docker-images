package main

import (
	"context"
	"crypto"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/big"
	"net"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"

	execute "github.com/alexellis/go-execute/pkg/v1"
	jwtgo "github.com/golang-jwt/jwt"
	cache "github.com/patrickmn/go-cache"
)

const (
	EnvOpenIDConfigURL = "OPENID_CONFIG_URL"
)

// CustomClaims ...
type CustomClaims struct {
	jwtgo.StandardClaims
}

// https://github.com/minio/minio/blob/a78bc7bfdbe20a58b0275803199afa76b3c4d769/internal/config/identity/openid/jwtgo.go#L317
type DiscoveryDoc struct {
	Issuer                           string   `json:"issuer,omitempty"`
	AuthEndpoint                     string   `json:"authorization_endpoint,omitempty"`
	TokenEndpoint                    string   `json:"token_endpoint,omitempty"`
	UserInfoEndpoint                 string   `json:"userinfo_endpoint,omitempty"`
	RevocationEndpoint               string   `json:"revocation_endpoint,omitempty"`
	JwksURI                          string   `json:"jwks_uri,omitempty"`
	ResponseTypesSupported           []string `json:"response_types_supported,omitempty"`
	SubjectTypesSupported            []string `json:"subject_types_supported,omitempty"`
	IDTokenSigningAlgValuesSupported []string `json:"id_token_signing_alg_values_supported,omitempty"`
	ScopesSupported                  []string `json:"scopes_supported,omitempty"`
	TokenEndpointAuthMethods         []string `json:"token_endpoint_auth_methods_supported,omitempty"`
	ClaimsSupported                  []string `json:"claims_supported,omitempty"`
	CodeChallengeMethodsSupported    []string `json:"code_challenge_methods_supported,omitempty"`
}

// JWKS - https://tools.ietf.org/html/rfc7517
// https://github.com/minio/minio/blob/1f262daf6fe369a57d8e183b3e3758644407e485/internal/config/identity/openid/jwks.go#L31
type JWKS struct {
	Keys []*JWKS `json:"keys,omitempty"`

	Kty string `json:"kty"`
	Use string `json:"use,omitempty"`
	Kid string `json:"kid,omitempty"`
	Alg string `json:"alg,omitempty"`

	Crv string `json:"crv,omitempty"`
	X   string `json:"x,omitempty"`
	Y   string `json:"y,omitempty"`
	D   string `json:"d,omitempty"`
	N   string `json:"n,omitempty"`
	E   string `json:"e,omitempty"`
	K   string `json:"k,omitempty"`
}

var (
	errMalformedJWKRSAKey = errors.New("malformed JWK RSA key")
	errMalformedJWKECKey  = errors.New("malformed JWK EC key")
)

// DecodePublicKey - decodes JSON Web Key (JWK) as public key
func (key *JWKS) DecodePublicKey() (crypto.PublicKey, error) {
	switch key.Kty {
	case "RSA":
		if key.N == "" || key.E == "" {
			return nil, errMalformedJWKRSAKey
		}

		// decode exponent
		ebuf, err := base64.RawURLEncoding.DecodeString(key.E)
		if err != nil {
			return nil, errMalformedJWKRSAKey
		}

		nbuf, err := base64.RawURLEncoding.DecodeString(key.N)
		if err != nil {
			return nil, errMalformedJWKRSAKey
		}

		var n, e big.Int

		n.SetBytes(nbuf)
		e.SetBytes(ebuf)

		return &rsa.PublicKey{
			E: int(e.Int64()),
			N: &n,
		}, nil
	case "EC":
		if key.Crv == "" || key.X == "" || key.Y == "" {
			return nil, errMalformedJWKECKey
		}

		var curve elliptic.Curve

		switch key.Crv {
		case "P-224":
			curve = elliptic.P224()
		case "P-256":
			curve = elliptic.P256()
		case "P-384":
			curve = elliptic.P384()
		case "P-521":
			curve = elliptic.P521()
		default:
			return nil, fmt.Errorf("Unknown curve type: %s", key.Crv)
		}

		xbuf, err := base64.RawURLEncoding.DecodeString(key.X)
		if err != nil {
			return nil, errMalformedJWKECKey
		}

		ybuf, err := base64.RawURLEncoding.DecodeString(key.Y)
		if err != nil {
			return nil, errMalformedJWKECKey
		}

		var x, y big.Int

		x.SetBytes(xbuf)
		y.SetBytes(ybuf)

		return &ecdsa.PublicKey{
			Curve: curve,
			X:     &x,
			Y:     &y,
		}, nil
	default:
		return nil, fmt.Errorf("Unknown JWK key type %s", key.Kty)
	}
}

// Validate token vs provider
func Validate(accessToken string, configURL string, c *cache.Cache) (string, error) {
	jp := new(jwtgo.Parser)
	jp.ValidMethods = []string{
		"RS256", "RS384", "RS512", "ES256", "ES384", "ES512",
		"RS3256", "RS3384", "RS3512", "ES3256", "ES3384", "ES3512",
	}

	// Validate token against issuer
	tt, _ := jwtgo.ParseWithClaims(accessToken, &CustomClaims{}, func(token *jwtgo.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwtgo.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}

		// check if publicKey already in cache
		pub, found := c.Get("key")
		if found {
			//fmt.Println("Using cached pubKey")

			return pub, nil
		}

		// Retrieve Issuer metadata from discovery endpoint
		d := DiscoveryDoc{}

		req, err := http.NewRequest(http.MethodGet, configURL, nil)
		if err != nil {
			return nil, err
		}
		clnt := http.Client{}

		r, err := clnt.Do(req)
		if err != nil {
			clnt.CloseIdleConnections()

			return nil, err
		}
		defer r.Body.Close()

		if r.StatusCode != http.StatusOK {
			return nil, errors.New(r.Status)
		}
		dec := json.NewDecoder(r.Body)
		if err = dec.Decode(&d); err != nil {
			return nil, err
		}

		// Get Public Key from JWK URI
		resp, err := clnt.Get(d.JwksURI)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			return nil, errors.New(resp.Status)
		}

		var jwk JWKS
		if err = json.NewDecoder(resp.Body).Decode(&jwk); err != nil {
			return nil, err
		}

		var kk crypto.PublicKey
		for _, key := range jwk.Keys {
			kk, err = key.DecodePublicKey()
			if err != nil {
				return nil, err
			}
		}

		// Return the rsa public key for the token validation
		pubKey := kk.(*rsa.PublicKey)

		c.Set("key", pubKey, cache.DefaultExpiration)

		return pubKey, nil

	})

	if claims, ok := tt.Claims.(*CustomClaims); ok && tt.Valid {
		log.Printf("%v", claims.Subject)

		return claims.Subject, nil
	} else {
		return "", fmt.Errorf("Invalid claim")
	}
}

var (
	privateMutex sync.RWMutex
	lockEnvMutex sync.Mutex
	envOff       bool
)

const (
	webEnvScheme       = "env"
	webEnvSchemeSecure = "env+tls"
)

var (
	globalRootCAs *x509.CertPool
)

// RegisterGlobalCAs register the global root CAs
func RegisterGlobalCAs(CAs *x509.CertPool) {
	globalRootCAs = CAs
}

var (
	hostKeys = regexp.MustCompile("^(https?://)(.*?):(.*?)@(.*?)$")
)

func fetchHTTPConstituentParts(u *url.URL) (username string, password string, envURL string, err error) {
	envURL = u.String()
	if hostKeys.MatchString(envURL) {
		parts := hostKeys.FindStringSubmatch(envURL)
		if len(parts) != 5 {
			return "", "", "", errors.New("invalid arguments")
		}
		username = parts[2]
		password = parts[3]
		envURL = fmt.Sprintf("%s%s", parts[1], parts[4])
	}

	if username == "" && password == "" && u.User != nil {
		username = u.User.Username()
		password, _ = u.User.Password()
	}
	return username, password, envURL, nil
}

func getEnvValueFromHTTP(urlStr, envKey string) (string, string, string, error) {
	u, err := url.Parse(urlStr)
	if err != nil {
		return "", "", "", err
	}

	switch u.Scheme {
	case webEnvScheme:
		u.Scheme = "http"
	case webEnvSchemeSecure:
		u.Scheme = "https"
	default:
		return "", "", "", errors.New("invalid arguments")
	}

	username, password, envURL, err := fetchHTTPConstituentParts(u)
	if err != nil {
		return "", "", "", err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, envURL+"?key="+envKey, nil)
	if err != nil {
		return "", "", "", err
	}

	claims := &jwtgo.StandardClaims{
		ExpiresAt: int64(15 * time.Minute),
		Issuer:    username,
		Subject:   envKey,
	}

	token := jwtgo.NewWithClaims(jwtgo.SigningMethodHS512, claims)
	ss, err := token.SignedString([]byte(password))

	if err != nil {
		return "", "", "", err
	}

	req.Header.Set("Authorization", "Bearer "+ss)

	clnt := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyFromEnvironment,
			DialContext: (&net.Dialer{
				Timeout:   3 * time.Second,
				KeepAlive: 5 * time.Second,
			}).DialContext,
			ResponseHeaderTimeout: 3 * time.Second,
			TLSHandshakeTimeout:   3 * time.Second,
			ExpectContinueTimeout: 3 * time.Second,
			TLSClientConfig: &tls.Config{
				RootCAs: globalRootCAs,
			},
			// Go net/http automatically unzip if content-type is
			// gzip disable this feature, as we are always interested
			// in raw stream.
			DisableCompression: true,
		},
	}

	resp, err := clnt.Do(req)
	if err != nil {
		return "", "", "", err
	}

	envValueBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", "", "", err
	}

	return string(envValueBytes), username, password, nil
}

// LookupEnv retrieves the value of the environment variable
// named by the key. If the variable is present in the
// environment the value (which may be empty) is returned
// and the boolean is true. Otherwise the returned value
// will be empty and the boolean will be false.
//
// Additionally if the input is env://username:password@remote:port/
// to fetch ENV values for the env value from a remote server.
// In this case, it also returns the credentials username and password
func LookupEnv(key string) (string, string, string, bool) {
	v, ok := os.LookupEnv(key)
	if ok && strings.HasPrefix(v, webEnvScheme) {
		// If env value starts with `env*://`
		// continue to parse and fetch from remote
		var err error
		v, user, pwd, err := getEnvValueFromHTTP(strings.TrimSpace(v), key)
		if err != nil {
			env, eok := os.LookupEnv("_" + key)
			if eok {
				// fallback to cached value if-any.
				return env, user, pwd, eok
			}
		}
		// Set the ENV value to _env value,
		// this value is a fallback in-case of
		// server restarts when webhook server
		// is down.
		os.Setenv("_"+key, v)
		return v, user, pwd, true
	}
	return v, "", "", ok
}

// Get retrieves the value of the environment variable named
// by the key. If the variable is present in the environment the
// value (which may be empty) is returned. Otherwise it returns
// the specified default value.
func envGet(key, defaultValue string) string {
	privateMutex.RLock()
	ok := envOff
	privateMutex.RUnlock()
	if ok {
		return defaultValue
	}
	if v, _, _, ok := LookupEnv(key); ok {
		return v
	}

	return defaultValue
}

func main() {
	configURL := envGet(EnvOpenIDConfigURL, "")

	c := cache.New(5*time.Minute, 10*time.Minute)

	http.HandleFunc("/htcondor", func(w http.ResponseWriter, r *http.Request) {
		tokenString := r.Header.Get("X-Auth-Request-Access-Token")
		if tokenString == "" {
			msg := fmt.Sprintln("No access token found in X-Auth-Request-Access-Token")
			http.Error(w, msg, http.StatusBadRequest)

			return

		}

		subject, err := Validate(tokenString, configURL, c)
		if err != nil {
			msg := fmt.Sprintf("Unable to validate token %s", err)
			http.Error(w, msg, http.StatusBadRequest)

			return
		}

		log.Println("Subject:", subject)

		// add user and mkdir
		cmd := execute.ExecTask{
			Command:     "useradd",
			Args:        []string{subject},
			StreamStdio: false,
		}

		res, err := cmd.Execute()
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
		}

		if res.ExitCode != 0 {
			http.Error(w, "Non-zero exit code: "+res.Stderr, http.StatusBadRequest)
		}

		io.WriteString(w, string("Autenticated!"))
	})
	log.Printf("About to listen on 8080.")

	err := http.ListenAndServe(":8080", nil)
	log.Fatal(err)
}
