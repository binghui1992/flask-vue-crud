from sqlalchemy import UUID
import sqlalchemy

from db import db


class Book(db.Model):
    __tablename__ = "book"
    # ensure being multiple imported will not cause exception
    __table_args__ = {"extend_existing": True}

    book_id = db.Column(UUID(as_uuid=True), primary_key=True,
                        server_default=sqlalchemy.text("uuid_generate_v4()"))
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))
    read = db.Column(db.Boolean)
    publish_date = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
