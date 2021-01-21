## Configuration

### Https frontend

Relevant parts in `./config/xrootd-http.cfg`:

```
if exec xrootd  
xrd.port 8443 
xrd.protocol XrdHttp:8443 libXrdHttp.so 
fi

ttp.header2cgi Authorization authz 
  
# Boiler-plate HTTPS configuration 
http.cadir /etc/grid-security/certificates
http.cert /etc/grid-security/hostcert.pem
http.key /etc/grid-security/hostcert.key
  
http.listingdeny yes 
http.staticpreload http://static/robots.txt /etc/xrootd/robots.txt 

```

### Scitoken config

Relevant parts in `./config/xrootd-http.cfg`:

```
ofs.authorize 
ofs.authlib libXrdAccSciTokens.so config=/etc/xrootd/scitokens.cfg 
  
# This particular authfile allows anonymous writes. 
acc.authdb /etc/xrootd/Auth-file-http
```

Relevant parts in `./config/scitokens.cfg`:

```
[Issuer VOTest] 
issuer = https://iam-escape.cloud.cnaf.infn.it/
base_path = / 
map_subject = False 
default_user = xrootd
```

### File staging

Relevant parts in `./config/xrootd-http.cfg`:

```
oss.remoteroot xroot://xrootd-cms.infn.it/

frm_xfragent  
frm.xfr.copycmd in noalloc url /tmp/scripts/xrdcp.sh $SRC?tried=+$CGI /data/$DST $HOST
```

`scripts/xrdcp.sh`:

```
#!/bin/bash  
echo "xrdcp -np $1 $2 $3" >> /tmp/copy.log  
xrdcp -np $1 $2 
```

### docker-compose

Nothing fancy here, just put the public IP of your server here to generate a selfsigned cert:

```
    environment:
      - XRD_HOST=__PUBLIC_HOST_HERE__
```

## Deployment

```bash
docker-compose up -d
```

### Test the instance

Install the `./ca/DODAS.pem` CA (or whatever ca did you use) in the client machine then do:

```
export TOKEN=`oidc-token --scope "storage.read:/" escape`
davix-get -H "Authorization: Bearer $TOKEN" https://__PUBLIC_HOST_HERE__:8443/__YOUR_LFN_HERE__ /tmp/data_test
```
