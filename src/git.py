from doit.tools import exceptions
import os

READY = '_git/ready'


def task_ready():
    """folder is ready for a new task?"""

    def git_is_ready():
        if os.system("git diff-index --quiet HEAD --") != 0:
            return exceptions.TaskFailed("Pending changes: commit or stash your workspace.")

    return {
        'basename': READY,
        'actions': [git_is_ready],
        'verbosity': 2
    }
