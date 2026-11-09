import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from app import create_app


class ContactApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database = Path(self.temp_dir.name) / "contacts.sqlite3"
        self.app = create_app({"TESTING": True, "DATABASE": str(database)})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_contact_submission_is_saved(self):
        response = self.client.post(
            "/api/contact",
            json={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "subject": "Hello",
                "message": "I would like to connect.",
            },
        )

        self.assertEqual(response.status_code, 201)
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            row = connection.execute(
                "SELECT name, email, subject, message FROM contact_messages"
            ).fetchone()
        self.assertEqual(
            row,
            ("Ada Lovelace", "ada@example.com", "Hello", "I would like to connect."),
        )

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            "/api/contact",
            json={"name": "Ada", "email": "invalid", "message": "Hello"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("valid email", response.get_json()["error"])

    def test_homepage_is_served(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Gasiram", response.data)
        response.close()

    def test_python_source_is_not_served(self):
        response = self.client.get("/app.py")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
