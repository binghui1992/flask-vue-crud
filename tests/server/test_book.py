import unittest

from server.app import create_app, db
from server.models.book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        app = create_app()

        # create test data
        book1 = Book(
            title="On the Road",
            author="Jack Kerouac",
            read=True,
            publish_date=None,
        )
        book2 = Book(
            title="Harry Potter and the Philosopher's Stone",
            author="J. K. Rowling",
            read=False,
            publish_date=None,
        )
        book3 = Book(
            title="Green Eggs and Ham",
            author="Dr. Seuss",
            read=True,
            publish_date=None,
        )

        with app.app_context():
            db.session.add(book1)
            db.session.add(book2)
            db.session.add(book3)
            db.session.commit()

        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        with self.app.app_context():
            # Drop all database tables
            db.drop_all()

    def test_crud(self):
        self._test_get_books()
        self._test_add_book()
        self._test_update_book()

    def _test_get_books(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(len(response.json["books"]), 3)
        self.assertEqual(response.json["books"][0]["title"], "On the Road")

    def _test_add_book(self):
        new_book = {"title": "A test book", "author": "Karl", "read": False}
        response = self.client.post("/books", json=new_book)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

        response = self.client.get("/books")
        self.assertEqual(len(response.json["books"]), 4)
        self.assertEqual(response.json["books"][-1]["title"], "A test book")

    def _test_update_book(self):
        response = self.client.get("/books")
        self.assertEqual(response.json["books"][-1]["read"], False)

        book_id = response.json["books"][-1]["book_id"]
        book_content = {"read": True}
        response = self.client.put(f"/books/{book_id}", json=book_content)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/books")
        self.assertEqual(response.json["books"][-1]["read"], True)

    def _test_delete_book(self):
        response = self.client.get("/books")
        book_id = response.json["books"][-1]["book_id"]
        response = self.client.delete(f"/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["books"]), 3)


if __name__ == "__main__":
    unittest.main()
