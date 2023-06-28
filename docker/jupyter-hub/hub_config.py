#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
#from oauthenticator.github import GitHubOAuthenticator
from oauthenticator.oauth2 import OAuthenticator
from oauthenticator.generic import GenericOAuthenticator
from tornado import gen
import subprocess
import warnings
import os
import jwt

from subprocess import check_call

c.JupyterHub.tornado_settings = {'max_body_size': 1048576000, 'max_buffer_size': 1048576000}
c.JupyterHub.log_level = 30

# 'http://141d9792-dee7-454e-93ef-89ae9ff07adc.k8s.civo.com:8888/hub/oauth_callback'
callback = os.environ["OAUTH_CALLBACK_URL"]
os.environ["OAUTH_CALLBACK"] = callback
iam_server = os.environ["OAUTH_ENDPOINT"]

s3_buckets = os.environ["S3_BUCKET"]
s3_endpoint = os.environ["S3_ENDPOINT"]

server_host = socket.gethostbyname(socket.getfqdn())
# TODO: run self registration then
#./.init/dodas-IAMClientRec
os.environ["IAM_INSTANCE"] = iam_server

myenv = os.environ.copy()

response = subprocess.check_output(['./.init/dodas-IAMClientRec', server_host], env=myenv)
response_list = response.decode('utf-8').split("\n")
client_id = response_list[len(response_list)-3]
client_secret = response_list[len(response_list)-2]

warnings.warn(response_list[len(response_list)-3])
warnings.warn(response_list[len(response_list)-2])

class EnvAuthenticator(GenericOAuthenticator):

    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        auth_state = yield user.get_auth_state()
        if "wlcg.groups" in auth_state["scope"]:
            groups = jwt.decode(auth_state["access_token"], options={"verify_signature": False})
            auth_state["oauth_user"]["groups"] = [ s[1:] for s in groups["wlcg.groups"] ]
        import pprint
        pprint.pprint(auth_state)
        if not auth_state:
            # user has no auth state
            return
        # define some environment variables from auth_state
        spawner.environment['ACCESS_TOKEN'] = auth_state['access_token']
        spawner.environment['REFRESH_TOKEN'] = auth_state['refresh_token']
        spawner.environment['USERNAME'] = auth_state['oauth_user']['preferred_username']
        spawner.environment['IAM_SERVER'] = iam_server
        spawner.environment['IAM_CLIENT_ID'] = client_id   
        spawner.environment['IAM_CLIENT_SECRET'] = client_secret
        spawner.environment['S3_BUCKETS'] = s3_buckets
        spawner.environment['S3_ENDPOINT'] = s3_endpoint

#c.JupyterHub.authenticator_class = GitHubEnvAuthenticator
        amIAllowed = False
        allowed_groups_user = ""
        allowed_groups_admin = ""
        matched_groups_user = False
        matched_groups_admin = False

        self.log.info(auth_state["oauth_user"])

        if auth_state["oauth_user"]["sub"] == os.environ["OAUTH_SUB"]:
            amIAllowed = True
        
        if os.environ.get("OAUTH_GROUPS"):
            spawner.environment["GROUPS"] = " ".join(auth_state["oauth_user"]["groups"])
            allowed_groups_user = os.environ["OAUTH_GROUPS"].split(" ")

            self.log.info("Allowed groups user")
            self.log.info(auth_state["oauth_user"]["groups"])
            self.log.info(allowed_groups_user)

            matched_groups_user = set(allowed_groups_user).intersection(set(auth_state["oauth_user"]["groups"])) 
                
        if os.environ["ADMIN_OAUTH_GROUPS"] :
            allowed_groups_admin = os.environ["ADMIN_OAUTH_GROUPS"].split(" ")            
            matched_groups_admin = set(allowed_groups_admin).intersection(set(auth_state["oauth_user"]["groups"])) 
            
            self.log.info("Allowed groups user")
            self.log.info(allowed_groups_admin)
            
        if matched_groups_user or matched_groups_admin : amIAllowed = True
                
        if not amIAllowed:
            err_msg = "Authorization Failed: User is not the owner of the service"
            if allowed_groups_user or allowed_groups_admin:
                err_msg =  err_msg + " nor belonging to the allowed groups %s %s" % (allowed_groups_user,allowed_groups_admin)
            self.log.error( err_msg )

            raise Exception( err_msg )

    # https://github.com/jupyterhub/oauthenticator/blob/master/oauthenticator/generic.py#L157
    async def authenticate(self, handler, data=None):
        code = handler.get_argument("code")

        params = dict(
            redirect_uri=self.get_callback_url(handler),
            code=code,
            grant_type="authorization_code",
        )
        params.update(self.extra_params)

        headers = self._get_headers()

        token_resp_json = await self._get_token(headers, params)

        user_data_resp_json = await self._get_user_data(token_resp_json)

        if callable(self.username_key):
            name = self.username_key(user_data_resp_json)
        else:
            name = user_data_resp_json.get(self.username_key)
            if not name:
                self.log.error(
                    "OAuth user contains no key %s: %s",
                    self.username_key,
                    user_data_resp_json,
                )
                return

        auth_state = self._create_auth_state(token_resp_json, user_data_resp_json)
        
        if "wlcg.groups" in auth_state["scope"]:
            groups = jwt.decode(auth_state["access_token"], options={"verify_signature": False})
            auth_state["oauth_user"]["groups"] = [ s[1:] for s in groups["wlcg.groups"] ]

        self.log.info(auth_state)
        
        is_admin = False
        matched_admin_groups = False 
        if os.environ["ADMIN_OAUTH_GROUPS"] :
            allowed_admin_groups = os.environ["ADMIN_OAUTH_GROUPS"].split(" ")            
            matched_admin_groups = set(allowed_admin_groups).intersection(set(auth_state["oauth_user"]["groups"])) 

        if os.environ.get("OAUTH_SUB") == auth_state["oauth_user"]["sub"]  or matched_admin_groups:
            self.log.info(
                "%s : is admin",
                ( name ),
            )
            is_admin = True
        else:
            self.log.info(" %s is not in admin of the service ", name)

        return {
            "name": name,
            "admin": is_admin,
            "auth_state": auth_state,  # self._create_auth_state(token_resp_json, user_data_resp_json)
        }

c.JupyterHub.authenticator_class = EnvAuthenticator
c.GenericOAuthenticator.oauth_callback_url = callback

# PUT IN SECRET
c.GenericOAuthenticator.client_id = client_id
c.GenericOAuthenticator.client_secret = client_secret 
c.GenericOAuthenticator.authorize_url = iam_server.strip('/') + '/authorize'
c.GenericOAuthenticator.token_url = iam_server.strip('/') + '/token'
c.GenericOAuthenticator.userdata_url = iam_server.strip('/') + '/userinfo'
c.GenericOAuthenticator.scope = ['openid', 'profile', 'email', 'address', 'offline_access', 'wlcg', 'wlcg.groups']
c.GenericOAuthenticator.username_key = "preferred_username"

c.GenericOAuthenticator.enable_auth_state = True
if 'JUPYTERHUB_CRYPT_KEY' not in os.environ:
    warnings.warn(
        "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
        "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
    )
    c.CryptKeeper.keys = [ os.urandom(32) ]

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.cmd = ['/opt/conda/bin/jupyterhub-singleuser', '--allow-root']
c.KubeSpawner.image = 'dodasts/spark:v3.0.3'

# TODO: PUT ENV

c.KubeSpawner.profile_list = [
    {
            'display_name': 'Small - 1CPU 2GB',
            'slug': 'training-python',
            'default': True,
            'kubespawner_override': {
                        'cpu_limit': 1.2,
                        'cpu_guarantee': 0.8,
                        'mem_guarantee': '1.8G',
                        'mem_limit': '2.2G',
                    }
        }, {
                'display_name': 'Medium - 2CPU 4GB',
                'slug': 'training-datascience',
                'kubespawner_override': {
                            'cpu_limit': 2.2,
                        'cpu_guarantee': 1.8,
                            'mem_limit': '4.5G',
                        'mem_guarantee': '3.8G',
                        }
        }, {
                'display_name': 'Large - 4CPU 8GB',
                'slug': 'training-datascience-2',
                'kubespawner_override': {
                            'cpu_limit': 4,
                        'cpu_guarantee': 3.5,
                            'mem_limit': '8G',
                        'mem_guarantee': '7G',
                        }
            }
]

c.KubeSpawner.privileged = True

c.KubeSpawner.extra_pod_config = {
    "automountServiceAccountToken": True,
         }

c.KubeSpawner.extra_container_config = {
    "securityContext": {
            "privileged": True,
            "capabilities": {
                        "add": ["SYS_ADMIN"]
                    }
        }
}
c.KubeSpawner.http_timeout = 600
c.KubeSpawner.start_timeout = 600

#  This is the address on which the proxy will bind. Sets protocol, ip, base_url
c.JupyterHub.bind_url = 'http://:8888'
c.JupyterHub.hub_ip = socket.gethostbyname(socket.getfqdn())
