import json
from fabric.api import env

with open("etc/deploy.json") as f:
    config = json.load(f)

env.use_ssh_config = True
env.git_url = config["deploy"]["giturl"]


def testing():
    """Testing environment."""
    env.env_type = 'testing'
    env.forward_agent = True
    env.roledefs = {
        "api": config["testing"]["server"]
    }
    env.base_dir = config["testing"]["basedir"].format(config)
    env.releases = "{}/releases".format(env.base_dir)
    env.current = "{}/current".format(env.base_dir)
    env.user = config["testing"]["user"]
    env.port = config["testing"]["port"]
    env.git_branch = config["testing"]["gitbranch"]

    env.config = {}
    try:
        with open("etc/testing/config.json") as f:
            env.config = json.load(f)
    except IOError:
        pass


def staging():
    """Staging environment."""
    env.env_type = 'staging'
    env.forward_agent = True
    env.roledefs = {
        "api": config["staging"]["server"]
    }
    env.base_dir = config["staging"]["basedir"].format(config)
    env.releases = "{}/releases".format(env.base_dir)
    env.current = "{}/current".format(env.base_dir)
    env.user = config["staging"]["user"]
    env.port = config["staging"]["port"]
    env.git_branch = config["staging"]["gitbranch"]

    env.config = {}
    try:
        with open("etc/staging/config.json") as f:
            env.config = json.load(f)
    except IOError:
        pass


def production():
    """Production environment."""
    env.env_type = 'production'
    env.forward_agent = True
    env.roledefs = {
        "api": config["production"]["server"]
    }
    env.base_dir = config["production"]["basedir"].format(config)
    env.releases = "{}/releases".format(env.base_dir)
    env.current = "{}/current".format(env.base_dir)
    env.user = config["production"]["user"]
    env.port = config["production"]["port"]
    env.git_tag = config["production"]["gittag"]

    env.config = {}
    try:
        with open("etc/production/config.json") as f:
            env.config = json.load(f)
    except IOError:
        pass
