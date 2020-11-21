#!/usr/bin/env python3

import requests
import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
import utils.github, utils.markdown, utils.writer
import markdown
import sys


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
        "-m",
        "--output-mode",
        dest="output_mode",
        help="Output destination",
        default="md",
        choices=["md", "html"],
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

    md_page = utils.github.fetch_page(args.md, gh_auth)

    gh_repos_set = utils.github.extract_repo_paths(
        utils.markdown.extract_urls_from_string(md_page)
    )

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(
            utils.github.fetch_repo_stats,
            gh_repos_set,
            [gh_auth] * len(gh_repos_set),
            timeout=60,
        )

        repo_stats = [
            r
            for r in results
            if type(r) is dict and r["stargazers_count"] >= args.star_threshold
        ]

        page_title = utils.markdown.extract_title_from_string(md_page)

        if page_title is None:
            page_title = args.md

        target_file = args.output

        if target_file is None:
            from slugify import slugify

            filename = slugify(page_title)
            target_file = f"./{filename}.{args.output_mode}"

        logging.info(f"Saving output to {target_file}")

        md_output = utils.markdown.format_repo_list(
            page_title,
            repo_stats,
        )

        with open(target_file, "w") as file:
            if args.output_mode == "md":
                utils.writer.write_md(target_file, md_output)
            elif args.output_mode == "html":
                html_output = markdown.markdown(md_output)
                utils.writer.write_html(target_file, page_title, html_output)
            else:
                logging.error(f"Can't output to {args.output_mode} format")
                sys.exit(1)

sys.exit(0)
