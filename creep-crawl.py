#!/usr/bin/env python3

import requests
import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from utils import github, markdown


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


if __name__ == "__main__":

    args = get_args()

    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s - %(message)s",
        level=args.level.upper(),
    )

    gh_auth = requests.auth.HTTPBasicAuth(args.gh_user, args.gh_password)

    md_page = github.fetch_page(args.md, gh_auth)

    gh_repos_set = github.extract_repo_paths(
        markdown.extract_urls_from_string(md_page)
    )

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(
            github.fetch_repo_stats,
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
            markdown.format_repo_list(
                markdown.extract_title_from_string(md_page),
                sorted_notable_repos,
            )
        )
