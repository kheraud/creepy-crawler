#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import daos.logic as db


# @TODO Add Patch repo with status / review_elements

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


app = Flask(
    __name__,
    static_folder="./dist/static",
    template_folder="./dist"
)

CORS(app)


@app.route("/pages", defaults={"path": None})
@app.route("/pages/<path:path>")
def pages(path):
    datas = db.fetch_aggregated_pages(path)[:]
    if path:
        if datas:
            return jsonify(datas[0])
        else:
            return jsonify({'error': 'Not Found'}), 404
    else:
        return jsonify(datas)


@app.route("/repos")
def repos():
    status = request.args.getlist("status", type=int)
    review_status = request.args.getlist("review_status", type=int)

    page = request.args.get("page", type=int)
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)
    sort_key = request.args.get("sort", type=str)

    repos = db.fetch_repositories(
        status if status else None,
        review_status if review_status else None,
        page if page else None,
        sort_key if sort_key else None,
        limit if limit else 100,
        offset if offset else 0,
    )[:]

    return jsonify(repos)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path):
    return render_template("index.html")


def serve(port):
    http_server = WSGIServer(("", port), app)
    http_server.serve_forever()


if __name__ == "__main__":

    configuration = get_args()

    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s - %(message)s",
        level=configuration.level.upper(),
    )

    init_database(configuration.database)

    try:
        serve(configuration.port)
    except KeyboardInterrupt:
        logging.info("Shutting down server")
