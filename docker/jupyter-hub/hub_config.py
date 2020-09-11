#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
#from oauthenticator.github import GitHubOAuthenticator
from oauthenticator.oauth2 import OAuthenticator
from oauthenticator.generic import GenericOAuthenticator
from tornado import gen
import warnings

import os

from subprocess import check_call

# 'http://141d9792-dee7-454e-93ef-89ae9ff07adc.k8s.civo.com:8888/hub/oauth_callback'
callback = os.environ["OAUTH_CALLBACK_URL"]

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
c.GenericOAuthenticator.client_id = '8bed0f49-168f-4c0d-8862-b11af06f2916'
c.GenericOAuthenticator.client_secret = 'G7yrGjR_qGcLWS44MadMUMj5xA9_bV1yRcFSdicUx9D0SeJVsGFfk0v5R0MPNT28gQWZ1QStwDe1r_8_xkeyDg'
c.GenericOAuthenticator.authorize_url = 'https://iam-demo.cloud.cnaf.infn.it/authorize'
c.GenericOAuthenticator.token_url = 'https://iam-demo.cloud.cnaf.infn.it/token'
c.GenericOAuthenticator.userdata_url = 'https://iam-demo.cloud.cnaf.infn.it/userinfo'
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
c.KubeSpawner.image = 'dciangot/hub:v2.4.5-rc31'

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

c.KubeSpawner.extra_container_config = {
    "securityContext": {
            "privileged": True,
            "capabilities": {
                        "add": ["SYS_ADMIN"]
                    }
        }
}
c.KubeSpawner.http_timeout = 300
c.KubeSpawner.start_timeout = 300

#  This is the address on which the proxy will bind. Sets protocol, ip, base_url
c.JupyterHub.bind_url = 'http://:8888'
c.JupyterHub.hub_ip = socket.gethostbyname(socket.getfqdn())
