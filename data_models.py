"""
data_models.py

Defines SQLAlchemy ORM models for Author and Book.
"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    """An author of one or more books."""
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Author id={self.id} name={self.name!r}>'

    def __str__(self):
        return self.name


class Book(db.Model):
    """A book with a title, ISBN, and link to its author."""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('authors.id'),
        nullable=False
    )

    author = db.relationship(
        'Author',
        backref=db.backref('books', lazy=True)
    )

    def __repr__(self):
        return f'<Book id={self.id} title={self.title!r} isbn={self.isbn!r}>'

    def __str__(self):
        return self.title
