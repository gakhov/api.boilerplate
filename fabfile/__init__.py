from fabric.api import roles

from .commands import deploy as _deploy, rollback as _rollback
from .environments import testing, staging, production

__all__ = [
    "deploy",
    "production",
    "staging",
    "testing",
    "rollback",
]


@roles('api')
def deploy(branch=None):
    """Deploy API to the server according the environment."""
    _deploy(branch)


@roles('api')
def rollback():
    """Rollback API on the server according the environment."""
    _rollback()
