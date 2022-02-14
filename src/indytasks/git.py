from doit.tools import exceptions
import os

READY = 'ready'

def task_ready():
    """folder is ready for a new task?"""

    def git_is_ready():
        if os.system("git diff-index --quiet HEAD --") != 0:
            os.system("git diff-index HEAD --")
            return exceptions.TaskFailed("Pending changes: commit or stash your workspace.")

    return {
        'basename': READY,
        'actions': ["git fetch", "git status", git_is_ready, "git checkout main"],
        'verbosity': 2
    }
