import sys
import os

sys.path.append('..')

import env

def get_premise():
    value = os.environ.get(env.PREMISE_ENV_VAR_NAME, None)
    return value if value != "NONE" else None

def set_premise(value):
    os.environ[env.PREMISE_ENV_VAR_NAME] = value