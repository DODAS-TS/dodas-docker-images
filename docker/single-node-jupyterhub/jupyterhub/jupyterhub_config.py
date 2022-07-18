# Configuration file for JupyterHub
import json
import os
import pathlib
import pprint
import socket
import subprocess
import sys
import warnings
import re

import dockerspawner
from oauthenticator.generic import GenericOAuthenticator
from tornado import gen

c = get_config()

c.JupyterHub.tornado_settings = {
    "max_body_size": 1048576000,
    "max_buffer_size": 1048576000,
}

callback = os.environ["OAUTH_CALLBACK_URL"]
os.environ["OAUTH_CALLBACK"] = callback
iam_server = os.environ["OAUTH_ENDPOINT"]

server_host = socket.gethostbyname(socket.getfqdn())
os.environ["IAM_INSTANCE"] = iam_server

# c.Spawner.default_url = '/lab'

myenv = os.environ.copy()

cache_file = "./cookies/iam_secret"

if os.path.isfile(cache_file):
    with open(cache_file) as f:
        cache_results = json.load(f)
else:
    response = subprocess.check_output(
        ["/.init/dodas-IAMClientRec", server_host], env=myenv
    )
    response_list = response.decode("utf-8").split("\n")
    client_id = response_list[len(response_list) - 3]
    client_secret = response_list[len(response_list) - 2]

    cache_results = {"client_id": client_id, "client_secret": client_secret}
    with open(cache_file, "w") as w:
        json.dump(cache_results, w)

client_id = cache_results["client_id"]
client_secret = cache_results["client_secret"]


class EnvAuthenticator(GenericOAuthenticator):
    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        auth_state = yield user.get_auth_state()

        pprint.pprint(auth_state)
        if not auth_state:
            # user has no auth state
            return
        # define some environment variables from auth_state
        self.log.info(auth_state)
        spawner.environment["IAM_SERVER"] = iam_server
        spawner.environment["IAM_CLIENT_ID"] = client_id
        spawner.environment["IAM_CLIENT_SECRET"] = client_secret
        spawner.environment["ACCESS_TOKEN"] = auth_state["access_token"]
        spawner.environment["REFRESH_TOKEN"] = auth_state["refresh_token"]
        spawner.environment["USERNAME"] = auth_state["oauth_user"]["preferred_username"]
        spawner.environment["JUPYTERHUB_ACTIVITY_INTERVAL"] = "15"

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
                err_msg =  err_msg + " nor belonging to the allowed groups %s %s" % (allowed_groups_user, allowed_groups_admin)
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

c.JupyterHub.db_url = "sqlite:///db/jupyterhub.sqlite"

# PUT IN SECRET
c.GenericOAuthenticator.client_id = client_id
c.GenericOAuthenticator.client_secret = client_secret
c.GenericOAuthenticator.authorize_url = iam_server.strip("/") + "/authorize"
c.GenericOAuthenticator.token_url = iam_server.strip("/") + "/token"
c.GenericOAuthenticator.userdata_url = iam_server.strip("/") + "/userinfo"
c.GenericOAuthenticator.scope = [
    "openid",
    "profile",
    "email",
    "address",
    "offline_access",
]
c.GenericOAuthenticator.username_key = "preferred_username"

c.GenericOAuthenticator.enable_auth_state = True
if "JUPYTERHUB_CRYPT_KEY" not in os.environ:
    warnings.warn(
        "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
        "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
    )
    c.CryptKeeper.keys = [os.urandom(32)]

c.JupyterHub.log_level = 30

c.JupyterHub.cookie_secret_file = "./cookies/jupyterhub_cookie_secret"

c.ConfigurableHTTPProxy.debug = True
c.JupyterHub.cleanup_servers = False
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.auth_token = os.environ.get("JUPYTER_PROXY_TOKEN", "test_token")
c.ConfigurableHTTPProxy.api_url = "http://http_proxy:8001"


_option_template = """
<label for="stack">Select your desired image:</label>
<input list="images" name="img">
<datalist id="images">
{images}
</datalist>

<br>
    
<label for="mem">Select your desired memory size:</label>
<select name="mem" size="1">
    {rams}
</select>

<br>

<label for="gpu">GPU:</label>
<select name="gpu" size="1">
    {gpu}
</select>
"""
# Spawn single-user servers as Docker containers
class CustomSpawner(dockerspawner.DockerSpawner):

    # ref: https://github.com/jupyterhub/dockerspawner/blob/87938e64fd3ca9a3e6170144fa6395502e3dba34/dockerspawner/dockerspawner.py#L309
    pull_policy = "always"

    def _options_form_default(self):
        # Get images
        images = os.environ.get("JUPYTER_IMAGE_LIST", "no default image")
        images = [image for image in images.split(",") if image]
        image_options = [
            f'<option value="{image}">{image.upper()}</option>' for image in images
        ]

        # Get ram sizes
        rams = os.environ.get("JUPYTER_RAM_LIST", "1G,2G,4G,8G")
        rams = [ram for ram in rams.split(",") if ram]
        ram_options = [f'<option value="{ram}">{ram}B</option>' for ram in rams]

        # Get GPU
        use_gpu: bool = os.environ.get("WITH_GPU", "false").lower() == "true"
        gpu_option = '<option value="N">Not Available</option>'
        if use_gpu:
            gpu_option = '<option value="Y">Yes</option>\n'
            gpu_option += '<option value="N"> No </option>'

        # Prepare template
        options = _option_template.format(
            images="\n".join(image_options),
            rams="\n".join(ram_options),
            gpu=gpu_option,
        )

        return options

    def options_from_form(self, formdata):
        options = {}
        options["img"] = formdata["img"]
        container_image = "".join(formdata["img"])
        print("SPAWN: " + container_image + " IMAGE")
        self.container_image = container_image
        options["mem"] = formdata["mem"]
        memory = "".join(formdata["mem"])
        self.mem_limit = memory
        options["gpu"] = formdata.get("gpu", "")
        use_gpu = "".join(options["gpu"]) == "Y"
        device_request = {}
        if use_gpu:
            device_request = {
                "Driver": "nvidia",
                "Capabilities": [
                    ["gpu"]
                ],  # not sure which capabilities are really needed
                "Count": 1,  # enable all gpus
            }
            self.extra_host_config = {
                "cap_add": ["SYS_ADMIN"],
                "privileged": True,
                "device_requests": [device_request],
            }
        else:
            self.extra_host_config = {"cap_add": ["SYS_ADMIN"], "privileged": True}
        return options

    @gen.coroutine
    def create_object(self):
        """Create the container/service object"""

        create_kwargs = dict(
            image=self.image,
            environment=self.get_env(),
            volumes=self.volume_mount_points,
            name=self.container_name,
            command=(yield self.get_command()),
        )

        # ensure internal port is exposed
        create_kwargs["ports"] = {"%i/tcp" % self.port: None}

        create_kwargs.update(self.extra_create_kwargs)

        # build the dictionary of keyword arguments for host_config
        host_config = dict(binds=self.volume_binds, links=self.links)

        if getattr(self, "mem_limit", None) is not None:
            # If jupyterhub version > 0.7, mem_limit is a traitlet that can
            # be directly configured. If so, use it to set mem_limit.
            # this will still be overriden by extra_host_config
            host_config["mem_limit"] = self.mem_limit

        if not self.use_internal_ip:
            host_config["port_bindings"] = {self.port: (self.host_ip,)}
        host_config.update(self.extra_host_config)
        host_config.setdefault("network_mode", self.network_name)

        self.log.debug("Starting host with config: %s", host_config)

        host_config = self.client.create_host_config(**host_config)
        create_kwargs.setdefault("host_config", {}).update(host_config)

        print(create_kwargs)
        # create the container
        obj = yield self.docker("create_container", **create_kwargs)
        return obj


c.JupyterHub.spawner_class = CustomSpawner

default_spawner = os.getenv("DEFAULT_SPAWNER", "LAB")
# Default spawn to jupyter noteook
spawn_cmd = os.environ.get(
    "DOCKER_SPAWN_CMD",
    "tini -s -- jupyterhub-singleuser --port=8889 --ip=0.0.0.0 --allow-root --debug --no-browser",
)
c.DockerSpawner.port = 8889

if default_spawner.upper() == "LAB":
    spawn_cmd += ' --SingleUserNotebookApp.default_url="/lab"'
    spawn_cmd += ' --NotebookApp.default_url="/lab"'
    spawn_cmd += ' --JupyterApp.config_file="/usr/etc/jupyter/jupyter_lab_config.py"'
    c.DockerSpawner.default_url = "/lab"

# uncomment to start a jupyter NB instead of jupyterlab
# spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "jupyterhub-singleuser --port 8889 --ip 0.0.0.0 --allow-root --debug")

c.DockerSpawner.extra_create_kwargs.update({"command": spawn_cmd})

post_start_cmd = os.getenv("POST_START_CMD", "")
if post_start_cmd:
    c.DockerSpawner.post_start_cmd = post_start_cmd

c.DockerSpawner.network_name = "jupyterhub"

c.DockerSpawner.http_timeout = 600

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
# notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
# c.DockerSpawner.notebook_dir = notebook_dir
# notebook_dir = "$PWD/persistent-area/{username}/"#os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
# c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
# c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

notebook_dir: str = os.environ.get("DOCKER_NOTEBOOK_DIR", "")
if notebook_dir == "":
    notebook_dir = "/jupyter-workspace"  # Default value

notebook_mount_dir = "/jupyter-mounts"  # Default value
notebook_mount_dir_prefix: str = os.environ.get("DOCKER_NOTEBOOK_MOUNT_DIR", "")
if notebook_mount_dir_prefix != "":
    notebook_mount_dir = notebook_mount_dir_prefix + "/jupyter-mounts"


collaborative_service: bool = os.getenv("JUPYTER_COLLAB_SERVICE", "False").lower() in [
    "true",
    "t",
    "yes",
]

volumes = {
    # Mount point for shared folder
    notebook_mount_dir
    + "/shared": {
        "bind": notebook_dir + "/shared",
        "mode": "ro",
    },
    notebook_mount_dir
    + "/shared/{username}": {
        "bind": notebook_dir + "/shared/{username}",
        "mode": "rw",
    },
    # Mount point for private stuff
    notebook_mount_dir
    + "/users/{username}/": {"bind": notebook_dir + "/private", "mode": "rw"},
}

volumes_collab = {
    # Mount point for collaboration jupyter lab
    notebook_mount_dir
    + "/collaborativefolder": {
        "bind": notebook_dir + "/collaborativefolder",
        "mode": "rw",
    },
    # notebook_mount_dir
    # + "/collaborativefolder/{username}": {
    #     "bind": notebook_dir + "/collaborativefolder/{username}",
    #     "mode": "rw",
    # },
}
if collaborative_service:
    c.DockerSpawner.volumes = {**volumes, **volumes_collab}
else:
    c.DockerSpawner.volumes = volumes

print(c.DockerSpawner.volumes)
use_cvmfs: bool = os.getenv("JUPYTER_WITH_CVMFS", "False").lower() in [
    "true",
    "t",
    "yes",
]
if use_cvmfs:
    c.DockerSpawner.volumes["/cvmfs/"] = {
        "bind": f"{notebook_dir}/cvmfs",
        "mode": "rw",
    }


# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

c.JupyterHub.hub_bind_url = "http://:8088"
c.JupyterHub.hub_connect_ip = "jupyterhub"

c.JupyterHub.admin_access = True

# c.Authenticator.allowed_users = {'test'}

services = [
    {
        "name": "idle-culler",
        "admin": True,
        "command": [sys.executable, "-m", "jupyterhub_idle_culler", "--timeout=7200"],
    },
]
if collaborative_service:
    services.append(
        {
            "url": "http://collab_proxy:8099",
            "name": "Collaborative-Jupyter",
            "api_token": os.environ.get("JUPYTERHUB_API_TOKEN", "API_TOKEN_EXAMPLE"),
        }
    )

c.JupyterHub.services = services
