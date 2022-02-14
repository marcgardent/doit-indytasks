

PLAN = "tf/plan"

def task_tf_plan():
    """terraform plan"""
    return {
        'basename': PLAN,
        'actions': [f"summon terraform plan"],
        'verbosity': 2,
        }
