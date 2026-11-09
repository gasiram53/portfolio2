import re
import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PUBLIC_EXTENSIONS = {
    ".css",
    ".html",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".pdf",
    ".png",
    ".svg",
    ".webp",
}


def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        DATABASE=str(Path(app.instance_path) / "contacts.sqlite3"),
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL DEFAULT '',
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()

    @app.get("/")
    def home():
        return send_from_directory(BASE_DIR, "index.html")

    @app.get("/<path:filename>")
    def site_files(filename):
        if Path(filename).suffix.lower() not in PUBLIC_EXTENSIONS:
            abort(404)
        return send_from_directory(BASE_DIR, filename)

    @app.post("/api/contact")
    def submit_contact():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Please submit the form as JSON."), 400

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject", "")
        message = data.get("message")
        if not all(isinstance(value, str) for value in (name, email, subject, message)):
            return jsonify(error="Please provide valid form values."), 400

        name, email, subject, message = (
            name.strip(),
            email.strip(),
            subject.strip(),
            message.strip(),
        )
        if not name or not email or not message:
            return jsonify(error="Name, email, and message are required."), 400
        if not EMAIL_PATTERN.fullmatch(email):
            return jsonify(error="Please provide a valid email address."), 400
        if len(name) > 100 or len(email) > 254 or len(subject) > 150 or len(message) > 5000:
            return jsonify(error="One or more fields exceed the allowed length."), 400

        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            connection.execute(
                """
                INSERT INTO contact_messages (name, email, subject, message)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, subject, message),
            )
            connection.commit()

        return jsonify(message="Thank you! Your message has been received."), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
