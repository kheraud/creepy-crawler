#!/usr/bin/env python3

import requests
import re
import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from io import StringIO


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", dest="gh_user", help="Github user")
    parser.add_argument(
        "-p", "--password", dest="gh_password", help="Github password"
    )
    parser.add_argument(
        "-t",
        "--star-threshold",
        dest="star_threshold",
        type=int,
        default=1000,
        help="Stars threshold",
    )
    parser.add_argument(
        "-o", "--output", dest="output", help="Output destination"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="warning",
        help="Log level",
    )
    parser.add_argument(
        "md", metavar="MD", help="Url to a remote Markdown to crawl"
    )

    return parser.parse_args()


def fetch_page(page_url, auth):

    r = requests.get(page_url, auth=auth)

    return r.text


def extract_md_urls_from_string(md):

    return re.findall(r"""\[[^\]]+\]\((https?:\/\/[^\s\)]+)""", md)


def extract_md_title_from_string(md):

    return re.search(r"""^#\s(.+)$""", md)


def extract_gh_repo_paths(url_list):

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


def fetch_gh_repo_stats(repo_path, auth):

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


def format_md(title, repo_stats):

    f = StringIO()

    f.write(f"# {title}  \n\n" "List of repositories :  \n\n")

    for stat in repo_stats:
        f.write(
            f"- [{stat['name']}]({stat['html_url']}) ({stat['full_name']}) : "
            f"{stat['description']}  \n"
            f"  **{stat['stargazers_count']}** ★, **{stat['forks_count']}**"
            f" fk., **{stat['open_issues_count']}** iss.\n"
        )

    return f.getvalue()


if __name__ == "__main__":

    args = get_args()

    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s - %(message)s",
        level=args.level.upper(),
    )

    gh_auth = requests.auth.HTTPBasicAuth(args.gh_user, args.gh_password)

    md_page = fetch_page(args.md, gh_auth)

    gh_repos_set = extract_gh_repo_paths(extract_md_urls_from_string(md_page))

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(
            fetch_gh_repo_stats,
            gh_repos_set,
            [gh_auth] * len(gh_repos_set),
            timeout=60,
        )

        repo_stats = [
            r
            for r in results
            if type(r) is dict and r["stargazers_count"] >= args.star_threshold
        ]

        sorted_notable_repos = sorted(
            repo_stats, key=lambda k: k["stargazers_count"], reverse=True
        )

        print(
            format_md(
                extract_md_title_from_string(md_page), sorted_notable_repos
            )
        )
