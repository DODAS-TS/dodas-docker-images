### Usage:
* ```docker-container up -d```
* ```docker attach tapev4```
* nel folder root bisogna esguire la richiesta di token con ```source oicd-setup.sh``` e poi eseguire ```./cygno_s32tape.sh```
* [monitor spazio](https://t1metria.cr.cnaf.infn.it/d/ZArHZvEMz/storage-usage-per-experiment?orgId=18&var-exp=cygn&var-vo=CYGNO)

### Tips for editing
```cd <script>```
```ssh -L 10000:localhost:10000 testnotebook```
```docker run -d -p 10000:8888 --name editor -v "${PWD}":/home/jovyan/work/ jupyter/scipy-notebook:9e63909e0317``` 
e poi avere il token di accesso guardate
```docker logs editor``` 


OLD

1) generare un tocken da qualunque macchina (la prima volta)
```
eval `oidc-agent-service use`
oidc-gen --issuer https://iam-t1-computing.cloud.cnaf.infn.it/ \
        --pw-cmd="echo pwd" --scope "openid profile email address phone offline_access eduperson_scoped_affiliation eduperson_entitlement" \
         t1-tape
```
1.1) richimare il tocken (le volte successive)
```
oidc-add t1-tape
```
2) prendere il token con 
```
oidc-token t1-tape
```
o, se la macchina con oidc e' la stessa, configirare
```
TOKEN=$(oidc-token t1-tape)
```
3) andare contnainer che gestisce il tape e copiare, come sotto, il token e esportare la varibaile BEARER_TOKEN
```
TOKEN=eyJraWQiOiJyc2ExIiwiYWxnI...

export BEARER_TOKEN=$TOKEN
```

* mail sistruzioni raw

~~~~
Buon pomeriggio,

come richiesto, abbiamo configurato una storage area tape esposta da StoRM WebDAV dedicata all'esperimento Cygno.

Per listare i file o scriverne di nuovi in questa storage area è necessario autenticarsi con un token rilasciato da un'istanza IAM che abbiamo al Tier1 condivisa fra vari esperimenti.

Sarà quindi necessario

- registrarsi su https://iam-t1-computing.cloud.cnaf.infn.it/login

- una volta registrati, fare richiesta attraverso https://iam-t1-computing.cloud.cnaf.infn.it di membership per il gruppo "Cygno".

Da command line (per esempio da ui-tier1) si può leggere/scrivere sulla storage area utilizzando tool come curl o gfal (più semplice e disponibile su ui-tier1), previa autenticazione.

L'autenticazione avviene secondo il modello a token, che è spiegato nella guida https://confluence.infn.it/display/TD/Data+transfers+using+http+endpoints#Datatransfersusinghttpendpoints-TokensWebDAV

Seguendo i passi descritti nella guida, sarà necessario:

- utilizzare OIDC-agent per registrare un client (solo la prima volta) che rilasci i token (oidc-gen)

- prendere un token (oidc-token)

- fare operazioni di data management/transfer ad esempio con gfal.

Abbiamo verificato che con un token rilasciato da iam-t1-computing per un utente (di User support) registrato nel gruppo Cygno, leggere, scrivere ed eliminare funzionano correttamente:

$ gfal-ls davs://xfer-archive.cr.cnaf.infn.it:8443/cygno

$ gfal-copy test davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/prova.txt

$ gfal-rm davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/prova.txt

Potete inoltre controllare lo stato di occupazione della storage area alla seguente pagina web:

https://t1metria.cr.cnaf.infn.it/d/ZArHZvEMz/storage-usage-per-experiment?orgId=18&var-exp=cygn&var-vo=CYGNO

Ovviamente, potete sempre contattare User support per problemi o difficoltà.

Cordiali saluti,

   Andrea
~~~~~

