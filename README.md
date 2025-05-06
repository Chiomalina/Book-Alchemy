# Book_Alchemy
# 📚 Book Alchemy

**Welcome to Book Alchemy** — a sleek, responsive Flask-based digital library application that lets you:

* ➕ **Add** authors and books (with ISBN, publication year, and dates).
* 🔍 **Search** your collection by title keyword (case-insensitive).
* 🔀 **Sort** your library by title or author.
* ❌ **Delete** books (and auto-cleanup authors without remaining books).
* 🖥 **Responsive UI** built with Bootstrap 5.

---

## 🚀 Quick Start

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/book-alchemy.git
   cd book-alchemy
   ```
2. **Create & activate** a virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database**

   * The app will auto-create `data/library.sqlite` on first run.
   * (Optional) Export a secret key:

     ```bash
     export SECRET_KEY="super-secret-value"
     ```
5. **Run the app**

   ```bash
   flask run --port=5001
   ```
6. **Browse** to `http://127.0.0.1:5001/` and start building your library!

---

## 🎨 UI & Templates

* **`templates/base.html`** — Base layout & navbar.
* **`templates/home.html`** — Dashboard with book cards, search bar, sort controls.
* **`templates/add_author.html`** & **`templates/add_book.html`** — Bootstrap-styled forms.
* **`static/`** (future): custom CSS or JS assets if needed.

---

## 🔧 Configuration

* **`app.config['SECRET_KEY']`** — Used for flashing messages and session security.
* **`SQLALCHEMY_DATABASE_URI`** — Points to `data/library.sqlite`.
* Set environment variables in `.env` (via **python-dotenv**) for production.

---

## 📚 Features & Roadmap

* [x] Add/View/Delete Authors & Books
* [x] Keyword Search & Sorting
* [x] Responsive UI with Bootstrap
* [ ] Detail pages for books & authors
* [ ] Cover image integration via ISBN API
* [ ] Edit & Pagination functionality

---

## 📝 Contributing

1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m "Add awesome feature"`.
4. Push to branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.

---

## ⚖️ License

This project is open-source and available under the **MIT License**. See [LICENSE](LICENSE) for details.

---

> Happy reading and coding! 📖✨
