# To install dependencies, run:
# pip install flask sqlalchemy flask_sqlalchemy jinja2
# To create the SQLite file, run:
# mkdir -p data && sqlite3 data/library.sqlite ".exit"

from flask import Flask
from data_models import db, Author, Book
import os

# Determine the base directory of the project
deploy_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(deploy_dir, 'data')

# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy to use the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize flask-sqlalchemy with our app and models
db.init_app(app)

# Example placeholder route
def index():
    return "Library app configured!"

if __name__ == '__main__':
    # Create tables within application context
    with app.app_context():
        db.create_all()
    app.run(debug=True)
