#!/usr/bin/env python3

import re
from io import StringIO


def extract_urls_from_string(md):

    return re.findall(r"""\[[^\]]+\]\((https?:\/\/[^\s\)]+)""", md)


def extract_title_from_string(md):

    return re.search(r"""^#\s(.+)$""", md)


def format_repo_list(title, repo_stats):

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
