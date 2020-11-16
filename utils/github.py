#!/usr/bin/env python3

import requests
import re
import logging


def fetch_page(page_url, auth):

    r = requests.get(page_url, auth=auth)

    return r.text


def extract_repo_paths(url_list):

    gh_repos = set()

    gh_url_regex = re.compile(r"""https?:\/\/github\.com\/([^\/]+/[^\/]+)""")

    for url in url_list:

        repository = gh_url_regex.match(url)

        if repository:
            gh_repos.add(repository.group(1))
        else:
            logging.debug(
                f"Skipping url {url} (link) cause not \
                            a valid github repository"
            )
            continue

    return gh_repos


def fetch_repo_stats(repo_path, auth):

    repo_api = requests.get(
        "https://api.github.com/repos/" + repo_path, auth=auth
    ).json()

    if all(
        key in repo_api
        for key in [
            "name",
            "full_name",
            "description",
            "html_url",
            "stargazers_count",
            "forks_count",
            "open_issues_count",
        ]
    ):
        logging.info(f"Scanned {repo_api['name']}")
        return {
            "name": repo_api["name"],
            "full_name": repo_api["full_name"],
            "description": repo_api["description"],
            "html_url": repo_api["html_url"],
            "stargazers_count": repo_api["stargazers_count"],
            "forks_count": repo_api["forks_count"],
            "open_issues_count": repo_api["open_issues_count"],
        }
    else:
        logging.warning(f"Can't find repo content for repo_path {repo_path}")
        return None
