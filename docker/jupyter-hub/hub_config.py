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

from subprocess import check_call

c.JupyterHub.tornado_settings = {'max_body_size': 1048576000, 'max_buffer_size': 1048576000}
c.JupyterHub.log_level = 30

# 'http://141d9792-dee7-454e-93ef-89ae9ff07adc.k8s.civo.com:8888/hub/oauth_callback'
callback = os.environ["OAUTH_CALLBACK_URL"]
os.environ["OAUTH_CALLBACK"] = callback
iam_server = os.environ["OAUTH_ENDPOINT"]

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
        import pprint
        pprint.pprint(auth_state)
        if not auth_state:
            # user has no auth state
            return
        # define some environment variables from auth_state
        spawner.environment['ACCESS_TOKEN'] = auth_state['access_token']
        spawner.environment['REFRESH_TOKEN'] = auth_state['refresh_token']
        spawner.environment['USERNAME'] = auth_state['oauth_user']['preferred_username']

#c.JupyterHub.authenticator_class = GitHubEnvAuthenticator
c.JupyterHub.authenticator_class = EnvAuthenticator
c.GenericOAuthenticator.oauth_callback_url = callback

# PUT IN SECRET
c.GenericOAuthenticator.client_id = client_id
c.GenericOAuthenticator.client_secret = client_secret 
c.GenericOAuthenticator.authorize_url = iam_server.strip('/') + '/authorize'
c.GenericOAuthenticator.token_url = iam_server.strip('/') + '/token'
c.GenericOAuthenticator.userdata_url = iam_server.strip('/') + '/userinfo'
c.GenericOAuthenticator.scope = ['openid', 'profile', 'email', 'address', 'offline_access']
c.GenericOAuthenticator.username_key = "preferred_username"

c.GenericOAuthenticator.enable_auth_state = True
if 'JUPYTERHUB_CRYPT_KEY' not in os.environ:
    warnings.warn(
        "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
        "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
    )
    c.CryptKeeper.keys = [ os.urandom(32) ]

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.cmd = ['jupyterhub-singleuser', '--allow-root']
c.KubeSpawner.image = 'dciangot/spark:good2'

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