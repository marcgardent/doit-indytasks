import re
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


READY = 'git/ready'
RELEASE = 'release'
CFG_FILE = "setup.cfg"
README_FILE = "README.md"

def replace_in_file(file, regex_source, regex_dest):     
    
    print(f"replace in '{file}' /{regex_source}/ by /{regex_dest}/ ...")
    content_new = ""
    
    with open (file, 'r', encoding='utf-8' ) as f:
        content_new = re.sub(regex_source, regex_dest, f.read(), flags = re.M)
    
    with open (file, 'w', encoding='utf-8' ) as f:
            f.write(content_new)

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

PACKAGE = "pack"
def task_package():
    """check the generation package locally"""
    return {
        'basename': PACKAGE,
        'targets': ["dist"],
        'actions': ["python -m build"],
        'verbosity': 2
    }



def task_release():
    """release new version"""

    def check_format(version):
        import re
        pattern = re.compile(r"^(\d+\.\d+\.\d+)$")
        return bool(pattern.match(version))

    def check_tag(version):
        ret = os.system(f"git rev-list v{version}") ==0
        if ret:
            print("tag already exists:")
            os.system("git tag --list")
            return exceptions.TaskFailed("change the version")

    def update_setup(version):
        replace_in_file(CFG_FILE, r'^version = \d+\.\d+\.\d+$',f"version = {version}")

    def update_readme(version):
        replace_in_file(README_FILE, r'@v\d+\.\d+\.\d+',f"@v{version}")

    def commit(version):
        cmd = f"git commit -a -m \"release version {version}\""
        print (cmd)
        return os.system(cmd) == 0

    def tag(version):
        cmd = f"git tag v{version} --sign -m \"release version {version}\""
        print (cmd)
        return os.system(cmd) == 0
            
    return {
        'basename': RELEASE,
        'params': [{'name': 'version', 'short': 'v', 'default': "0.0.0"}],
        'task_dep': [READY, PACKAGE],
        'targets': [CFG_FILE, README_FILE],
        'actions': [(check_format,), (check_tag,), (update_setup,), (update_readme,), (commit,), (tag,), "git push --porcelain", "git push --tags --porcelain"],
        'verbosity': 2
    }
