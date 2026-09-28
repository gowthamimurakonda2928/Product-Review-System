from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'product-review-secret-key'


def create_database():
    connection = sqlite3.connect('reviews.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            product TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/reviews/<product>')
def reviews(product):
    connection = sqlite3.connect('reviews.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT * FROM reviews WHERE LOWER(product) = LOWER(?)',
        (product,)
    )

    reviews_data = cursor.fetchall()
    connection.close()

    return render_template(
        'reviews.html',
        reviews=reviews_data,
        product=product
    )


@app.route('/add_review')
def add_review():
    return render_template('add_review.html')


@app.route('/add_review', methods=['POST'])
def submit_review():
    name = request.form['name']
    product = request.form['product']
    rating = request.form['rating']
    review = request.form['review']

    connection = sqlite3.connect('reviews.db')
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO reviews (name, product, rating, review) VALUES (?, ?, ?, ?)',
        (name, product, rating, review)
    )

    connection.commit()
    connection.close()

    return render_template(
        'reviews.html',
        reviews=[(0, name, product, rating, review)],
        product=product
    )


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def submit_register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    connection = sqlite3.connect('reviews.db')
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
        (username, email, password)
    )

    connection.commit()
    connection.close()

    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def submit_login():
    username = request.form['username']
    password = request.form['password']

    connection = sqlite3.connect('reviews.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        session['username'] = username
        return render_template('index.html')
    else:
        return "Invalid username or password"


if __name__ == '__main__':
    create_database()

    app.run(debug=True)

