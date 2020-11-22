#!/usr/bin/env python3

from argparse import ArgumentParser
import daos.logic as db
import logging
import sys

def get_args():
    parser = ArgumentParser()
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

    return parser.parse_args()

def init_database(db_path):
    db.init_database(db_path)
    db.create_schema()
    logging.debug("Database initialized")

if __name__ == "__main__":

    configuration = get_args()

    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s - %(message)s",
        level=configuration.level.upper(),
    )

    init_database(configuration.database)

    for repo in db.fetch_repositories(2):
        print(repo)
