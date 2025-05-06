
from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
import os
import secrets
from datetime import datetime


# Set up project directory and database path
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')

# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

# Full path to SQLite file
db_path = os.path.join(data_dir, 'library.sqlite')

# Initialize Flask app
app = Flask(__name__)
# SECRET_KEY is critical for session security and should be unpredictable.
# In production, set the SECRET_KEY environment variable; otherwise, generate a random one at startup.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Use absolute path for SQLite URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind SQLAlchemy to Flask app
db.init_app(app)

# Define routes here (add_author, add_book, home, etc.)
@app.route('/')
def home():
    # get sort parameters from querystring
    sort = request.args.get('sort', 'title')  # default sort by title
    if sort == 'author':
        # join to Author and order by Author.name
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()

    return render_template('home.html', books=books, current_sort=sort)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        # Grab the raw strings
        birth_str = request.form.get('birth_date')
        death_str = request.form.get('date_of_death')

        # Convert to date objects (or None)
        birth_date = (
            datetime.strptime(birth_str, "%Y-%m-%d").date()
            if birth_str else None
        )
        date_of_death = (
            datetime.strptime(death_str, "%Y-%m-%d").date()
            if death_str else None
        )

        author = Author(name=name,
                        birth_date=birth_date,
                        date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()
        flash(f'Author "{author.name}" added successfully!', 'success')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.order_by(Author.name).all()

    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        pub_year = request.form.get('publication_year') or None
        author_id = request.form['author_id']

        book = Book(isbn=isbn,
                    title=title,
                    publication_year=pub_year,
                    author_id=author_id)
        db.session.add(book)
        db.session.commit()
        flash(f'Book "{book.title}" added successfully!', 'success')
        return redirect(url_for('add_book'))

    return render_template('add_book.html', authors=authors)

if __name__ == '__main__':
     app.run(port=5001, debug=True)
    # Create tables before the first request by initializing them here
    # with app.app_context():
    #     db.create_all()




