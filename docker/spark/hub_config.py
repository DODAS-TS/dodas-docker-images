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

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.cmd = ['jupyterhub-singleuser', '--allow-root']
c.KubeSpawner.image = 'dciangot/spark:test14'

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

#c.KubeSpawner.cpu_guarantee = 1.5
#c.KubeSpawner.cpu_limit = 2
#c.KubeSpawner.mem_guarantee = '2G'
#c.KubeSpawner.mem_limit = '4G'
c.KubeSpawner.extra_containers = [{
        "name": "master",
        "image": "dciangot/spark:test15",
        "command": ["/bin/sh", "-c"],
        "args": ["/usr/local/spark/bin/spark-class org.apache.spark.deploy.master.Master"],
        "env": [
        ],
    }]

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
