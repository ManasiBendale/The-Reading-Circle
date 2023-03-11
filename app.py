from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from passlib.hash import sha256_crypt

app = Flask(__name__)

# app.jinja_env.filters['zip'] = zip
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'test1'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test1'

app.config['MYSQL_HOST'] = 'flaskdb.cviupmaskxl1.us-east-1.rds.amazonaws.com:3306'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin1234'
app.config['MYSQL_DB'] = 'flaskaws'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin1234@swaptable.cgurkhcysih2.us-west-2.rds.amazonaws.com/swaptable'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"


# engine = create_engine('mysql://root:''@localhost/flaskaws')
# connection = engine.raw_connection()
# cursor = connection.cursor()
db = SQLAlchemy(app)
mysql = MySQL(app)
# db = MySQL(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    participation = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password, participation):
        self.username = username
        self.password = password
        self.email = email
        self.participation = participation


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_link = db.Column(db.String(500))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, author, category, image_link, userid):
        self.title = title
        self.author = author
        self.category = category
        self.image_link = image_link
        self.userid = userid


class Swap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    main_owner = db.Column(db.String(100))
    new_owner = db.Column(db.String(500))
    bookid = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, main_owner, new_owner, bookid, userid):
        self.title = title
        self.main_owner = main_owner
        self.new_owner = new_owner
        self.bookid = bookid
        self.userid = userid


@app.route('/')
@app.route('/main')
def main():
    # books = Book.query.all()
    return render_template('main.html')


@app.route('/request')
def request_book():
    books = Book.query.all()
    users = User.query.all()
    flash("You have successfully requested this book!", "success")
    return render_template('index.html', books=books, users=users)


@app.route('/show')
def show():
    books = Book.query.all()
    users = User.query.all()
    return render_template('show.html', books=books, users=users)


@app.route('/index')
def index():
    books = Book.query.all()
    users = User.query.all()
    return render_template('index.html', books=books, users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        secure_password = sha256_crypt.encrypt(str(password))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE username = % s', [username, ])
        account = cursor.fetchone()
        print("1ST PASSWORD:", password)
        print("2ND PASSWORD: ", secure_password)
        if account:
            if sha256_crypt.verify(password, secure_password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                flash('Logged in successfully !', "success")
                return redirect(url_for('index'))
            else:
                flash(
                    'Login unsuccessful! Your account or password must be wrong!', "danger")
                return render_template('login.html')
        else:
            flash('Login unsuccessful! Account does not exist!', "danger")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash("User logged out successfully")
    return redirect(url_for('main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'participation' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        participation = request.form['participation']
        secure_password = sha256_crypt.encrypt(str(password))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            flash('Account already exists !', "danger")
        elif not username or not password or not email:
            flash('Please fill out the form !', "danger")
        else:
            cursor.execute(
                'INSERT INTO user VALUES (NULL, % s, % s, % s,% s)', (username, secure_password, email, participation, ))
            mysql.connection.commit()
            flash('You have successfully registered !', "success")
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/add/', methods=['POST'])
def insert_book():
    if request.method == "POST":
        book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            category=request.form.get('category'),
            image_link=request.form.get('image_link'),
            userid=session['id']
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully")
        return redirect(url_for('index'))


@app.route('/update/', methods=['POST'])
def update():
    if request.method == "POST":
        my_data = Book.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']

        db.session.commit()
        flash("Book is updated")
        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book is deleted")
    return redirect(url_for('index'))


@app.route('/choose_book/', methods=['POST'])
def choose_book():
    if request.method == "POST":

        book = Swap(
            title=request.form.get('title'),
            main_owner=session['username'],
            new_owner=session['username'],
            bookid=request.form.get('bookid'),
            userid=session['id']
        )
        db.session.add(book)
        db.session.commit()
        flash("Book chosen successfully!", "success")
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
