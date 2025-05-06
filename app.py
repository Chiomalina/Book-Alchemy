"""
app.py

Flask application for managing a simple digital library:
- Add, list, search, and delete books and authors.
"""

import os
import secrets
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

from data_models import Author, Book, db


# ------------------------------------------------------------------------------
# App & database setup
# ------------------------------------------------------------------------------

# Base directory and data path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# SQLite database file
DB_PATH = os.path.join(DATA_DIR, 'library.sqlite')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------


@app.route('/')
def home():
    """Display (and optionally search/sort) the list of books."""
    query = Book.query.join(Author)

    # Keyword search
    search_term = request.args.get('q', '').strip()
    if search_term:
        pattern = f'%{search_term}%'
        query = query.filter(Book.title.ilike(pattern))

    # Sorting
    sort = request.args.get('sort', 'title')
    if sort == 'author':
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()
    return render_template(
        'home.html',
        books=books,
        q=search_term,
        current_sort=sort
    )


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Form to add a new author (with optional birth/death dates)."""
    if request.method == 'POST':
        name = request.form['name']
        birth_str = request.form.get('birth_date', '')
        death_str = request.form.get('date_of_death', '')

        birth_date = (
            datetime.strptime(birth_str, '%Y-%m-%d').date()
            if birth_str else None
        )
        death_date = (
            datetime.strptime(death_str, '%Y-%m-%d').date()
            if death_str else None
        )

        author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=death_date
        )
        db.session.add(author)
        db.session.commit()
        flash(f'Author "{author.name}" added.', 'success')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Form to add a new book, selecting from existing authors."""
    authors = Author.query.order_by(Author.name).all()

    if request.method == 'POST':
        book = Book(
            isbn=request.form['isbn'],
            title=request.form['title'],
            publication_year=request.form.get('publication_year') or None,
            author_id=request.form['author_id']
        )
        db.session.add(book)
        db.session.commit()
        flash(f'Book "{book.title}" added.', 'success')
        return redirect(url_for('add_book'))

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book (and its author if no books remain)."""
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    # Remove author if they have no remaining books
    if not Book.query.filter_by(author_id=author.id).count():
        db.session.delete(author)
        db.session.commit()
        flash(
            f'Book "{book.title}" and author "{author.name}" removed.',
            'success'
        )
    else:
        flash(f'Book "{book.title}" deleted.', 'success')

    return redirect(url_for('home'))


if __name__ == '__main__':
     app.run(port=5001, debug=True)
    # Create tables before the first request by initializing them here
    # with app.app_context():
    #     db.create_all()




