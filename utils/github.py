#!/usr/bin/env python3

import requests
import re
from .exception import NetworkError


def check_auth(user, password) -> bool:
    me = requests.get(
        "https://api.github.com/user",
        auth=requests.auth.HTTPBasicAuth(user, password),
    )
    if me.status_code == 200:
        return True

    return False


def fetch_page(page_url, user, password):

    auth = None

    if user and password:
        auth = requests.auth.HTTPBasicAuth(user, password)

    r = requests.get(
        page_url,
        auth=auth,
    )

    if r.status_code != 200:
        raise NetworkError(f"Status {r.status_code}, Body '{r.text}'")

    return r.text


def extract_repo_paths(url_list):

    gh_repos = set()

    gh_url_regex = re.compile(r"""https?:\/\/github\.com\/([^\/]+/[^\/]+)""")

    for url in url_list:

        repository = gh_url_regex.match(url)

        if repository:
            gh_repos.add(repository.group(1))
        else:
            continue

    return gh_repos


def fetch_repo_stats(repo_path, user, password):

    repo_api = requests.get(
        "https://api.github.com/repos/" + repo_path,
        auth=requests.auth.HTTPBasicAuth(user, password),
    ).json()

    if all(
        key in repo_api
        for key in [
            "name",
            "description",
            "html_url",
            "stargazers_count",
            "forks_count",
            "open_issues_count",
        ]
    ):
        return {
            "name": repo_api["name"],
            "description": repo_api["description"],
            "html_url": repo_api["html_url"],
            "stargazers_count": repo_api["stargazers_count"],
            "forks_count": repo_api["forks_count"],
            "open_issues_count": repo_api["open_issues_count"],
        }
    else:
        return None
