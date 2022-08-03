Custum test Docker for CYGNO


* info: https://confluence.infn.it/pages/viewpage.action?spaceKey=INFNCLOUD&title=Estenzione+e+Customizzazione+immagini+docker+CYGNO
* docker build -t mydockerhubuser/mycustomimage:myversion /docker/path (non Dockerfile ma il path alla directory)
* il docker-compose.yaml sulla VM sta in /usr/local/share/dodasts/jupyterhub/
* esempio 
```
docker build -t gmazzitelli/cygno-lab:v1.0.14-cygno /Users/mazzitel/cygno_dev/dodas-docker-images/docker/CYGNO/custom/
docker push gmazzitelli/cygno-lab:v1.0.14-cygno
```
* convien fare il pull sulla macchina
```
ssh 192.135.24.159
cd /usr/local/share/dodasts/jupyterhub/
sudo vi docker-compose.yaml (aggiornare il docker))
sudo docker pull gmazzitelli/cygno-lab:v1.0.14-cygno
```

* test https://192.135.24.159:8888/
* per mettere piu' versioni aggiornare la variabile come nell'esempio in usr/local/share/dodasts/jupyterhub/docker-compose.yaml: 
```
- JUPYTER_IMAGE_LIST=gmazzitelli/cygno-lab:v1.0.14-cygno,dodasts/cygno-lab:v1.0.16-cygno
```
* per riunire la branch locale con il muster da cui si e' forkato (https://stackoverflow.com/questions/7244321/how-do-i-update-or-sync-a-forked-repository-on-github) a me a funzionato solo il mage
```
# Add the remote, call it "upstream":

git remote add upstream https://github.com/whoever/whatever.git

# Fetch all the branches of that remote into remote-tracking branches

git fetch upstream

# Make sure that you're on your master branch:

git checkout master

# Rewrite your master branch so that any commits of yours that
# aren't already in upstream/master are replayed on top of that
# other branch:

git merge --no-ff upstream/master 
```
* per la build completa:
```
cd /Users/mazzitel/dodas-docker-images/docker/CYGNO
docker build -t gmazzitelli/cygno-lab:v1.0.17-cygno -f lab/Dockerfile .
docker push gmazzitelli/cygno-lab:v1.0.17-cygno
```
