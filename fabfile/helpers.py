import os.path
from fabric.api import cd, env, run


def supervisor(command, subdir=None):
    """Run a supervisor command."""
    run_dir = env.current
    if subdir:
        run_dir = os.path.join(run_dir, subdir)

    if run('if [ -d %s ]; then echo y; else echo n; fi' % run_dir) == 'y':
        with cd(run_dir):
            run('bin/supervisorctl %s' % command)
