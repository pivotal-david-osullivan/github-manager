import os
import json
from .runner import GhRunner

REPO_CONFIG_OSS = os.path.expanduser('~/.ghm/repos.json')
REPO_CONFIG_TZ = os.path.expanduser('~/.ghm/repos-tanzu.json')

def fetch_buildpack_toml(repo):
    import urllib.request
    import subprocess

    fp = urllib.request.urlopen(
        f"https://raw.githubusercontent.com/{repo}/main/buildpack.toml")
    cmd = ["yj", "-tj"]
    res = subprocess.run(cmd, capture_output=True, check=True, input=fp.read())
    return json.loads(res.stdout)


def check_requirements():
    from subprocess import CalledProcessError
    try:
        GhRunner().help()
        return True
    except CalledProcessError:
        return False


def load_repos(remote_repos=False, org=None, repo_src='OSS'):
    """Loads a JSON formatted list of repositories to be used by the script"""
    if remote_repos:
        repos = GhRunner().list_repos(org=org)
        return [repo['full_name'] for repo in repos
                if 'full_name' in repo.keys()]
    else:
        if repo_src == 'OSS':
           repos = json.load(open(REPO_CONFIG_OSS))
        elif repo_src == 'TZ' :
           repos = json.load(open(REPO_CONFIG_TZ))

        if not hasattr(repos, "append") or not hasattr(repos, "__len__"):
            raise TypeError("Invalid configuration file")
        return repos
