
from indytasks import git
UPGRADE = 'py/upgrade'
INSTALL = 'py/install'
FREEZE = '_py/freeze'

class R:
    REQUIREMENTS = "requirements.txt"
    REQUIREMENTS_LOCK = "requirements.lock.txt"

def task_py_install():
    """install python dependencies"""
    return {
        'basename': INSTALL,
        'actions': [f"pip3 install -r {R.REQUIREMENTS}"],
        'file_dep': [R.REQUIREMENTS],
        'verbosity': 2,
        }

def task_py_freeze():
    """freeze python dependencies"""
    return {
        'basename': FREEZE,
        'actions': [f"pip3 freeze > {R.REQUIREMENTS_LOCK}"],
        'verbosity': 2,
        'targets': [R.REQUIREMENTS_LOCK]
        }

def task_py_upgrade():
    """upgrade python dependencies"""
    
    return {
        'basename' : UPGRADE, 
        'task_dep': [git.READY, INSTALL, FREEZE],
        'actions': ["echo upgrade done: check and commit changes."],
        'verbosity': 2
        }
