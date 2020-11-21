#!/usr/bin/env python3

import re
from io import StringIO


def extract_urls_from_string(md):

    return re.findall(r"""\[[^\]]+\]\((https?:\/\/[^\s\)]+)""", md)


def extract_title_from_string(md):

    matched = re.search(r"""^#\s([^\[]+)""", md, flags=re.MULTILINE)

    if matched:
        return matched.group(1).strip()

    return None


def format_repo_list(title, repo_stats):

    sorted_notable_repos = sorted(
        repo_stats, key=lambda k: k["stargazers_count"], reverse=True
    )

    f = StringIO()

    f.write(f"# {title}  \n\n" "List of repositories :  \n\n")

    for stat in sorted_notable_repos:
        f.write(
            f"- [{stat['name']}]({stat['html_url']}) ({stat['full_name']}) : "
            f"{stat['description']}  \n"
            f"  **{stat['stargazers_count']}** ★, **{stat['forks_count']}**"
            f" fk., **{stat['open_issues_count']}** iss.\n"
        )

    return f.getvalue()
