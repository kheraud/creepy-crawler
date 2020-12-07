#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
from concurrent.futures import ThreadPoolExecutor
import utils.github
import utils.markdown
import utils.writer
import datetime
import daos.logic as db
import sys, os


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-u",
        "--github-user",
        dest="gh_user",
        default=os.environ.get("GITHUB_USER"),
        metavar="GITHUB_USER",
        help="Github user",
    )
    parser.add_argument(
        "-p",
        "--github-password",
        dest="gh_password",
        default=os.environ.get("GITHUB_PASSWORD"),
        metavar="GITHUB_PASSWORD",
        help="Github password",
    )
    parser.add_argument(
        "-c",
        "--crawl-min-age",
        dest="crawl_min_age",
        type=int,
        default=86400,
        help="Skip repositories last crawled before this duration of seconds",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        nargs="?",
        default=None,
        help="Output destination",
    )
    parser.add_argument(
        "-d",
        "--database",
        dest="database",
        help="Path to SQLite database",
        default="app.db",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Log level",
    )
    parser.add_argument(
        "md", metavar="MD", help="Url to a remote Markdown to crawl"
    )

    return parser.parse_args()


def init_database(db_path):
    db.init_database(db_path)
    db.create_schema()
    logging.debug("Database initialized")


def get_repositories_to_crawl(md_page, crawl_min_age):

    gh_repos_set = set(
        map(
            str.lower,
            utils.github.extract_repo_paths(
                utils.markdown.extract_urls_from_string(md_page)
            ),
        )
    )

    count_initial_repo = len(gh_repos_set)
    now = datetime.datetime.now()

    for existing_repo in db.match_repositories_by_names(gh_repos_set):
        since_last_crawl = (now - existing_repo["crawl_date"]).total_seconds()

        if since_last_crawl < crawl_min_age:
            logging.debug(
                f"Removing {existing_repo['name']} from crawl,"
                f"last crawl {int(since_last_crawl)} sec. ago"
            )
            gh_repos_set.discard(existing_repo["name"])

    logging.info(
        f"{count_initial_repo - len(gh_repos_set)} repo removed from crawl cause already crawled recently"
    )

    return gh_repos_set


def save_output(target_file, page_title, repo_stats):
    logging.info(f"Saving output to {target_file}")
    utils.writer.write_md(
        target_file,
        utils.markdown.format_repo_list(
            page_title,
            repo_stats,
        ),
    )


def update_repo_stats(page_id, repo_path, user, password):
    stats = utils.github.fetch_repo_stats(repo_path, user, password)

    if stats:
        logging.debug(f"Repository {repo_path} fetched")
        db.add_repository(
            page_id,
            repo_path,
            stats["html_url"],
            stats["description"],
            datetime.datetime.now(),
            stats["stargazers_count"],
            stats["forks_count"],
            stats["open_issues_count"],
        )
        logging.debug(f"Repository {repo_path} stored in db")
    else:
        logging.warning(f"Can't fetch repository {repo_path}")

    return stats


if __name__ == "__main__":

    configuration = get_args()

    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s - %(message)s",
        level=configuration.level.upper(),
    )

    md_page = utils.github.fetch_page(
        configuration.md, configuration.gh_user, configuration.gh_password
    )

    init_database(configuration.database)

    page_title = utils.markdown.extract_title_from_string(md_page)

    if page_title is None:
        page_title = configuration.md

    # Create page reference with a None crawl end date
    crawl_start_date = datetime.datetime.now()
    page_id = db.add_page(
        configuration.md, page_title, datetime.datetime.now(), None
    )
    logging.debug(f"Page info stored in db with id {page_id}")

    repos_to_crawl = get_repositories_to_crawl(
        md_page, configuration.crawl_min_age
    )

    count_repo_to_crawl = len(repos_to_crawl)

    logging.info(f"Start crawling {count_repo_to_crawl} repositories")

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(
            update_repo_stats,
            [page_id] * count_repo_to_crawl,
            repos_to_crawl,
            [configuration.gh_user] * count_repo_to_crawl,
            [configuration.gh_password] * count_repo_to_crawl,
            timeout=300,
        )

        repo_stats = [r for r in results if type(r) is dict]

        logging.info(f"End of crawling {len(repos_to_crawl)} repositories")

        # Update page reference with a real end date
        db.add_page(
            configuration.md,
            page_title,
            crawl_start_date,
            datetime.datetime.now(),
        )

        if configuration.output:
            save_output(configuration.output, page_title, repo_stats)

sys.exit(0)
