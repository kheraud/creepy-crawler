#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import daos.logic as db
from daos.schema import ReviewSchema
from marshmallow import ValidationError
import os

MAX_LIMIT_REPOSITORY = 200
DEFAULT_LIMIT_REPOSITORY = 25


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--database",
        dest="database",
        help="Path to SQLite database",
        default=os.environ.get("DB_PATH"),
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="level",
        choices=["debug", "info", "warning", "error", "critical"],
        default=os.environ.get("LOG_LEVEL"),
        help="Log level",
    )
    parser.add_argument(
        "-e",
        "--mode",
        dest="mode",
        choices=["development", "test", "production"],
        default=os.environ.get("APP_ENV"),
        metavar="APP_ENV",
        help="Environment mode (environment variable APP_ENV)",
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=5000,
        help="Server port",
    )

    return parser.parse_args()


def init_database(db_path):
    db.init_database(db_path)
    db.create_schema()


app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")

CORS(app)


@app.route("/api/pages", defaults={"path": None})
@app.route("/api/pages/<path:path>")
def pages(path):
    datas = db.fetch_aggregated_pages(path)[:]
    if path:
        if datas:
            return jsonify(datas[0])
        else:
            return jsonify({"error": "Not Found"}), 404
    else:
        return jsonify(datas)


@app.route("/api/repos")
def repos():
    status = request.args.getlist("status", type=int)
    status = status if status else None

    page = request.args.get("page", type=int)

    sort_key = request.args.get("sort", type=str)

    limit = request.args.get("limit", type=int)
    limit = (
        min(limit, MAX_LIMIT_REPOSITORY) if limit else DEFAULT_LIMIT_REPOSITORY
    )

    offset = request.args.get("offset", type=int)
    offset = offset if offset else 0

    repos = db.fetch_repositories(
        status if status else None,
        page,
        sort_key if sort_key else None,
        limit,
        offset,
    )[:]

    response = {
        "metadata": {
            "limit": limit,
            "offset": offset,
            "count": len(repos),
            "total": db.fetch_repositories_count(
                status,
                page,
            ),
        },
        "results": repos,
    }

    return jsonify(response)


repo_review_schema = ReviewSchema()


@app.route("/api/repos/<int:repo_id>", methods=["PATCH"])
def patch_repo(repo_id):
    # Does this repo exists
    target_repo = db.fetch_repository(repo_id)

    if not target_repo:
        return jsonify({"error": "Not Found"}), 404

    json_input = request.json

    try:
        review = repo_review_schema.load(json_input)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    target_repo.status = review["status"]

    if "review_comment" in review:
        target_repo.review_comment = review["review_comment"]

    db.update_repository(target_repo)

    return "", 200


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path):
    return render_template("index.html")


def serve(mode, port):
    if mode == "development":
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        http_server = WSGIServer(("", port), app)
        http_server.serve_forever()


if __name__ == "__main__":

    configuration = get_args()

    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s - %(message)s",
        level=configuration.level.upper(),
    )

    logging.info(f"Application started in {configuration.mode} mode")

    init_database(configuration.database)

    try:
        serve(configuration.mode, configuration.port)
    except KeyboardInterrupt:
        logging.info("Shutting down server")
