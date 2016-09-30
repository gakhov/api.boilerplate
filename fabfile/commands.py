from datetime import datetime
import os.path

from fabric.api import abort, cd, env, run, settings

from .helpers import supervisor

VERSION_DIR_FORMAT = "%Y-%m-%d.%H%M"


def _is_version(path):
    """Check if the path is a version."""
    name = os.path.basename(path.rstrip("/"))
    try:
        datetime.strptime(name, VERSION_DIR_FORMAT)
        return True
    except:
        pass
    return False


def deploy(branch=None, subdir=None):
    """Deploy the backend and start supervisor.

    :param branch: The branch to use. If `None`, it will use the default
                   branch from the configuration.
    :param subdir: The subdirectory to build in. If `None`, this will be
                   the same as the deployment directory, i.e. the git
                   repository"s root directory.

    """
    new_version_dir = "%s/%s" % (env.releases,
                                 datetime.now().strftime(VERSION_DIR_FORMAT))
    run("mkdir -p %s" % new_version_dir)

    # prepare or updated the cached copy
    run("git clone %s %s" % (env.git_url, new_version_dir))

    # based on the environment we deploy a certain branch/tag from git
    with cd(new_version_dir):
        if env.env_type == "testing":
            git_branch = branch or env.git_branch
            if not git_branch:
                abort("In 'testing' environment only branches to be deployed")
            if git_branch != "master":
                run("git checkout -b {branch} origin/{branch}".format(
                    branch=git_branch))
        elif env.env_type == "staging":
            if not env.git_branch:
                abort("In 'staging' environment only branches to be deployed")
            if env.git_branch != "master":
                run("git checkout -b %(git_branch)s origin/%(git_branch)s" %
                    env)
        elif env.env_type == "production":
            if not env.git_tag:
                abort("In 'production' environment only tags to be deployed")
            run("git checkout -b tag-%(git_tag)s %(git_tag)s" % env)

    build_dir = new_version_dir
    if subdir:
        build_dir = os.path.join(new_version_dir, subdir)

    with cd(build_dir):
        run("make")
        run("bin/buildout -c {}.cfg".format(env.env_type))
        if env.env_type == "testing":
            run("make test")
        else:
            run("all-tests")

        run("docs")
        run("swagger")

    # Stop the current running version
    with settings(warn_only=True):
        supervisor("shutdown", subdir=subdir)

    # reset the `current` link to the new version
    with cd(env.base_dir):
        run("rm -f current && ln -s %s current" % new_version_dir)

    # Start the new version
    with cd(build_dir):
        run("bin/supervisord && sleep 1")

    cleanup(max_to_keep=5)


def rollback():
    """Rollback the current version to the version before."""
    with cd(env.base_dir):
        current_version = run("readlink current | sed 's/.*\/\(.*\)/\\1/'")

        # try to get the previous version
        releases = run("ls -t releases").split("\t")
        for i in xrange(len(releases)):
            if releases[i].endswith(current_version):
                previous_version = releases[i + 1]

        # stop the `current` version
        with settings(warn_only=True):
            supervisor("shutdown")

        # install the `old` version
        with cd(env.base_dir):
            run("rm current && ln -s %s/%s current" % (env.releases,
                                                       previous_version))

        # start the `new` version
        with cd(env.current):
            run("bin/supervisord && sleep 1")


def cleanup(max_to_keep=5):
    """Keep only max_to_keep newest versions."""
    dir_ = os.path.join(env.releases, "")
    string_ = run("for i in %s*; do echo $i; done" % dir_)
    candidates = string_.replace("\r", "").split("\n")
    if len(candidates) <= max_to_keep:
        return

    versions = filter(_is_version, candidates)
    versions.sort(reverse=True)
    for version in versions[max_to_keep:]:
        run("rm -rf %s" % version)
