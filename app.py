import random
from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from passlib.hash import sha256_crypt
import base64
from jinja2 import Environment

app = Flask(__name__)

app.jinja_env.filters['zip'] = zip
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test5'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"


db = SQLAlchemy(app)
mysql = MySQL(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    participation = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password, participation, city):
        self.username = username
        self.password = password
        self.email = email
        self.city = city
        self.participation = participation


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(40), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(100), nullable=False)
    image_link = db.Column(db.String(100), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(100), db.ForeignKey(
        'user.username'), nullable=False)

    def __init__(self, title, author, category, image_link, summary, rating, userid, user_name):
        self.title = title
        self.author = author
        self.category = category
        self.image_link = image_link
        self.summary = summary
        self.rating = rating
        self.userid = userid
        self.user_name = user_name


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
    swaps = Swap.query.all()
    return render_template('show.html', books=books, users=users, swaps=swaps)


@app.route('/index')
def index():
    books = Book.query.all()
    users = User.query.all()
    swaps = Swap.query.all()
    return render_template('index.html', books=books, users=users, swaps=swaps)


@app.route('/navbar')
def navbar():
    books = Book.query.all()
    users = User.query.all()
    swaps = Swap.query.all()
    return render_template('navbar.html', books=books, users=users, swaps=swaps)


# USER DETAILS--------------------------------------------------------------------------------------------------------------------------------------------------------------

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
    # flash("User logged out successfully")
    return redirect(url_for('main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'participation' in request.form and 'city' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        city = request.form['city']
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
                'INSERT INTO user VALUES (NULL, % s, % s, % s,% s,% s)', (username, secure_password, email, city, participation, ))
            mysql.connection.commit()
            flash('You have successfully registered !', "success")
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/update_profile/', methods=['POST'])
def update_profile():
    if request.method == "POST":
        my_data = User.query.get(request.form.get('id'))
        my_data.username = request.form['username']
        my_data.email = request.form['email']
        my_data.city = request.form['city']
        my_data.participation = request.form['participation']

        db.session.commit()
        flash("Profile is updated!")
        return redirect(url_for('index'))

# USER DETAILS---------------------------------------------------------------------------------------------------------------------------------------------------------------------


# BOOK DETAILS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/add/', methods=['POST'])
def insert_book():
    if request.method == "POST":
        image_file = request.files['pdf']
        image_data = image_file.read()
        pdf_data_b64 = base64.b64encode(image_data).decode("utf-8")

        book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            summary=request.form.get('summary'),
            category=request.form.get('category'),
            rating=request.form.get('rating'),
            image_link=pdf_data_b64,
            userid=session['id'],
            user_name="Need to fill"
        )
        db.session.add(book)
        tempid = book.userid
        print("TEMP", tempid)
        userdata = User.query.get(tempid)
        print("USERDATA", userdata)
        new = userdata.username
        print("NEW:", new)
        book.user_name = userdata.username
        db.session.commit()
        flash("Book added successfully")
        return redirect(url_for('index'))


@app.route('/update/', methods=['POST'])
def update():
    if request.method == "POST":
        my_data = Book.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.summary = request.form['summary']
        my_data.category = request.form['category']
        my_data.rating = request.form['rating']
        # my_data.image_link = request.form['image_link']

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

# BOOK DETAILS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


# SWAP DETAILS----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/choose_book/', methods=['POST'])
def choose_book():
    if request.method == "POST":
        my_data = Book.query.get(request.form.get('id'))

        book = Swap(
            title="Need to fill",
            main_owner=session['username'],
            new_owner=session['username'],
            bookid=request.form.get('bookid'),
            userid=session['id']
        )
        db.session.add(book)
        booktitle = book.bookid
        my_data = Book.query.get(booktitle)
        new = my_data.title
        print(new)
        book.title = my_data.title
        db.session.commit()
        flash("Book chosen successfully!", "success")
        return redirect(url_for('index'))


@app.route('/swap_page')
def swap_page():
    swaps = Swap.query.all()
    return render_template('user_swap_page.html', swaps=swaps)


@app.route('/swap_book/')
def swap_book():
    # Get all Swap objects from the database
    swaps = Swap.query.all()

    # Create a list of (id, main_owner, new_owner) tuples
    swap_data = [(swap.id, swap.main_owner, swap.new_owner) for swap in swaps]
    print("OG:", swap_data)
    # Shuffle the list of tuples
    random.shuffle(swap_data)

    swapped_owners = {}

    # Loop through the shuffled swap data tuples
    for i, (swap_id, main_owner, new_owner) in enumerate(swap_data):
        # Get a new owner that is not the same as the main owner and has not been swapped before
        new_new_owner = None
        while not new_new_owner or new_new_owner == main_owner or (new_new_owner, main_owner) in swapped_owners.values():
            new_new_owner = random.choice(
                [swap[1] for swap in swap_data if swap[1] != main_owner and swap[0] != swap_id])
        print("NEW OWNER--------------------------------------------------------:", new_new_owner)

        # Swap the main_owner and new_owner values
        Swap.query.filter_by(id=swap_id).update(
            {'main_owner': new_owner, 'new_owner': new_new_owner})

        # Add the swapped owners to the swapped_owners dictionary
        swapped_owners[i] = (new_owner, new_new_owner)

    # Commit the changes to the database
    db.session.commit()

    # Render the template with the swapped owners data
    return render_template('swap.html', swapped_owners=swapped_owners)

    # # Swap main_owner and new_owner values, avoiding repeats
    # for i in range(len(swap_data)):
    #     current_swap = swap_data[i]
    #     print("Current Swap:", current_swap)
    #     next_swap = swap_data[(i+1) % len(swap_data)]
    #     print("Next Swap:", next_swap)

    #     # Avoid repeating owners
    #     while next_swap[1] == current_swap[2] or next_swap[2] == current_swap[1]:
    #         random.shuffle(swap_data)
    #         current_swap = swap_data[i]
    #         print("Current Swap-------------------------:", current_swap)
    #         next_swap = swap_data[(i+1) % len(swap_data)]
    #         print("Next Swap-------------------------:", next_swap)

    #     # Swap owners
    #     current_swap = (current_swap[0], current_swap[2], current_swap[1])
    #     next_swap = (next_swap[0], next_swap[2], next_swap[1])

    #     # Update Swap objects in the database
    #     Swap.query.filter_by(id=current_swap[0]).update(
    #         {'main_owner': current_swap[1], 'new_owner': current_swap[2]})
    #     Swap.query.filter_by(id=next_swap[0]).update(
    #         {'main_owner': next_swap[1], 'new_owner': next_swap[2]})

    # # Commit changes to the database
    # db.session.commit()
    # return render_template('swap.html')


# @app.route('/swap_book/')
# def swap_book():
#     swaps = Swap.query.all()
#     import random

#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute(
#         'SELECT id, title, main_owner, new_owner, bookid, userid FROM swap')
#     records1 = cursor.fetchall()
#     keys = ['id', 'title', 'main_owner', 'new_owner', 'bookid', 'userid']
#     l = [[row[key] for key in keys] for row in records1]
#     print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", l)
#     swapped_with = []

#     def shuffle_records(records):
#         shuffled_records = random.sample(records, len(records))
#         return shuffled_records

#     def book_swap(l):
#         records = [(record[0], record[3], record[5], record[2])
#                    for record in l]
#         shuffled = shuffle_records(records)
#         swapped = set()

#         # swapped table
#         for i, record in enumerate(l):
#             # temp = record[3]
#             # print("Previous owner : ", temp)
#             while (record[0], shuffled[i][1]) in swapped or shuffled[i][1] == record[2] or shuffled[i][3] == record[3]:
#                 random.shuffle(shuffled)

#             print("shuffled[i][1]", shuffled[i][1])
#             record[3] = shuffled[i][1]
#             swapped.add((record[0], record[3]))
#             swapped_with.append([record[0], record[3]])
#             # print("qwertyuiopxcvbnm", [record[3], temp])
#             # swapped_with.append([record[3], temp])
#         return l, swapped_with

#     l, swapped_books = book_swap(l)
#     for i in range(0, len(l)-1):
#         swaps[i].new_owner = swapped_books[i][1]

#     db.session.commit()
#     return render_template('swap.html', l=l, swapped_books=swapped_books, swaps=swaps)


if __name__ == "__main__":
    app.run(debug=True)
