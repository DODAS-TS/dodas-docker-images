package main

import (
	"crypto"
	"crypto/rsa"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"

	execute "github.com/alexellis/go-execute/pkg/v1"
	jwtgo "github.com/dgrijalva/jwt-go"
	"github.com/minio/minio/cmd/config/identity/openid"
	"github.com/minio/minio/pkg/env"
	cache "github.com/patrickmn/go-cache"
)

const (
	EnvOpenIDConfigURL = "OPENID_CONFIG_URL"
)

var ()

// CustomClaims ...
type CustomClaims struct {
	jwtgo.StandardClaims
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
		d := openid.DiscoveryDoc{}

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

		var jwk openid.JWKS
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

func main() {
	configURL := env.Get(EnvOpenIDConfigURL, "")

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
