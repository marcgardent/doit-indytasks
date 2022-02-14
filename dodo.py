from doit.tools import exceptions
import os

READY = 'git/ready'
RELEASE = 'release'
CFG_FILE = "setup.cfg"

def task_ready():
    """folder is ready for a new task?"""

    def git_is_ready():
        if os.system("git diff-index --quiet HEAD --") != 0:
            return exceptions.TaskFailed("Pending changes: commit or stash your workspace.")

    return {
        'basename': READY,
        'actions': [git_is_ready, "git pull"],
        'verbosity': 2
    }

def task_release():
    """release new version"""

    def check_format(version):
        import re
        pattern = re.compile(r"^(\d+\.\d+\.\d+)$")
        return bool(pattern.match(version))

    def update_setup(version):     
        import re           
        with open (CFG_FILE, 'r' ) as f:
            content = f.read()
            content_new = re.sub(r'version = \d+\.\d+\.\d+', f'version = {version}', content, flags = re.M)
            print(content_new)

    return {
        'basename': RELEASE,
        'params': [{'name': 'version', 'short': 'v', 'default': "0.0.0"}],
        'task_dep': [],
        'file_dep': [CFG_FILE],
        'actions': [(check_format,), (update_setup,)],
        'verbosity': 2
    }
