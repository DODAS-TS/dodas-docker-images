from ._version import __version__ 

def _jupyter_nbextension_paths():
    """ Used by "jupyter nbextension" command to install frontend extension """
    return [dict(
                section="notebook",
                src="nbextension",
                dest="sparkconnector",
                require="sparkconnector/extension"),
            ]

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "@swan-cern/sparkconnector"
    }]

def _jupyter_server_extension_paths():
    """ Used by "jupyter serverextension" command to install web server extension """
    return [{
        "module": "sparkconnector.portallocator"
    }]

