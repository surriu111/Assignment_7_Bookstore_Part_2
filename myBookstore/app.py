from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import os

# instantiate the app
app = Flask(__name__, static_folder='static')

def get_db_connection(): 
    conn = sqlite3.connect('bookstore.db') 
    conn.row_factory = sqlite3.Row 
    print('successful connected')
    return conn

def get_categories(): 
    conn = get_db_connection() 
    categories = conn.execute("SELECT * FROM categories").fetchall() 
    conn.close() 
    return categories

# set up routes
@app.route('/') 
def home(): 
    return render_template("index.html", categories=get_categories())

@app.route('/category') 
def category(): 
    category_id = request.args.get("categoryId", type=int) 
 
    conn = get_db_connection() 
    books = conn.execute( 
        "SELECT * FROM books WHERE categoryId = ?", 
        (category_id,) 
    ).fetchall() 
    conn.close() 
 
    return render_template( 
        "category.html", 
        selected_category=category_id, 
        categories=get_categories(), 
        books=books 
    )

@app.route('/search', methods=['POST']) 
def search(): 
    term = request.form.get("search", "").strip() 
 
    conn = get_db_connection() 
    books = conn.execute( 
        "SELECT * FROM books WHERE lower(title) LIKE lower(?)", 
        (f"%{term}%",) 
    ).fetchall() 
    conn.close() 
 
    return render_template( 
        "search.html", 
        categories=get_categories(), 
        books=books, 
        term=term 
    )

@app.route('/book/<int:book_id>') 
def book_detail(book_id): 
    conn = get_db_connection() 
    book = conn.execute(""" 
        SELECT books.*, categories.name AS categoryName 
        FROM books 
        JOIN categories ON categories.id = books.categoryId 
        WHERE books.id = ? 
    """, (book_id,)).fetchone() 
    conn.close() 
 
    return render_template("bookDetail.html", book=book)

@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    app.run(debug = True)
    # the prot is 5000 as default

#  python app.py