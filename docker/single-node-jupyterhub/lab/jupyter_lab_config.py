import os

from jupyter_core.utils import ensure_dir_exists
from notebook.services.contents.largefilemanager import LargeFileManager
from notebook.services.contents.filecheckpoints import GenericFileCheckpoints


class CustomCheckpointFolder(GenericFileCheckpoints):
    checkpoint_dir = "/jupyter-checkpoints"

    # Ref: https://github.com/jupyter/notebook/blob/2cfff07a39fa486a3f05c26b400fa26e1802a053/notebook/services/contents/filecheckpoints.py#L104
    def checkpoint_path(self, checkpoint_id, path):
        """find the path to a checkpoint"""
        path = path.strip("/")
        parent, name = ("/" + path).rsplit("/", 1)
        parent = parent.strip("/")
        basename, ext = os.path.splitext(name)
        filename = u"{name}-{checkpoint_id}{ext}".format(
            name=basename,
            checkpoint_id=checkpoint_id,
            ext=ext,
        )
        os_path = self._get_os_path(path=parent)
        cp_dir = os.path.join(
            os_path, self.checkpoint_dir, parent
        )  # Add parent directory to checkpoint_dir
        with self.perm_to_403():
            ensure_dir_exists(cp_dir)
        cp_path = os.path.join(cp_dir, filename)
        return cp_path


class CustomFileManager(LargeFileManager):
    checkpoints_class = CustomCheckpointFolder


# c.ServerApp.contents_manager_class = CustomFileManager # TODO: bench test

c.ServerApp.terminado_settings = {"shell_command": ["/usr/bin/bash"]}

c.ResourceUseDisplay.track_cpu_percent = True
