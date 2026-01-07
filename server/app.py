#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# If your lab already imports db/Article from models, use that instead.
from models import db, Article

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# REQUIRED for session cookies
app.secret_key = "super-secret-key"

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)


@app.get("/articles/<int:id>")
def get_article(id):
    # 1) initialize page views if missing
    session["page_views"] = session.get("page_views") or 0

    # 2) increment on every request
    session["page_views"] += 1

    # 3) enforce paywall (max 3 views allowed)
    if session["page_views"] > 3:
        return make_response(
            jsonify({"message": "Maximum pageview limit reached"}),
            401,
        )

    # 4) return article JSON if under the limit
    article = Article.query.get(id)
    if article is None:
        return make_response(jsonify({"message": "Article not found"}), 404)

    return make_response(jsonify(article.to_dict()), 200)


@app.get("/clear")
def clear_session():
    session.clear()
    return make_response(jsonify({"message": "Session cleared"}), 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
