from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import hashlib
import random
import string
import secrets

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("instance/database.db")

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        user = request.form['username']

        pwd = hashlib.sha256(
            request.form['password'].encode()
        ).hexdigest()

        db = get_db()
        cur = db.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, pwd)
        )

        data = cur.fetchone()

        if data:

            session['user'] = user

            return redirect('/dashboard')

        else:

            return render_template(
                "login.html",
                error="Invalid ID or Password"
            )

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        user = request.form['username']

        pwd = hashlib.sha256(
            request.form['password'].encode()
        ).hexdigest()

        db = get_db()
        cur = db.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=?",
            (user,)
        )

        if cur.fetchone():

            return render_template(
                'register.html',
                error="This ID already exists"
            )

        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user, pwd)
        )

        db.commit()

        return redirect('/')

    return render_template('register.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user' not in session:
        return redirect('/')

    db = get_db()

    if request.method == 'POST':

        site = request.form['site']

        username = request.form['username']

        password = request.form['password']

        db.execute(
            "INSERT INTO passwords (user, site, username, password) VALUES (?, ?, ?, ?)",
            (session['user'], site, username, password)
        )

        db.commit()

    cur = db.cursor()

    cur.execute(
        "SELECT id, site, username, password FROM passwords WHERE user=?",
        (session['user'],)
    )

    data = cur.fetchall()

    return render_template(
        'dashboard.html',
        data=data
    )


@app.route('/saved-passwords')
def saved_passwords():

    if 'user' not in session:
        return redirect('/')

    db = get_db()

    cur = db.cursor()

    cur.execute(
        "SELECT id, site, username, password FROM passwords WHERE user=?",
        (session['user'],)
    )

    data = cur.fetchall()

    return render_template(
        'saved_password.html',
        data=data
    )


@app.route('/edit-password/<int:id>', methods=['GET', 'POST'])
def edit_password(id):

    if 'user' not in session:
        return redirect('/')

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM passwords WHERE id=? AND user=?",
        (id, session['user'])
    )

    data = cur.fetchone()

    if not data:
        return redirect('/saved-passwords')

    if request.method == 'POST':

        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        current_password = data[4]

        if old_password != current_password:

            return render_template(
                'edit_password.html',
                error="Old password is incorrect"
            )

        if new_password != confirm_password:

            return render_template(
                'edit_password.html',
                error="New passwords do not match"
            )

        cur.execute(
            "UPDATE passwords SET password=? WHERE id=?",
            (new_password, id)
        )

        db.commit()

        return redirect('/saved-passwords')

    return render_template(
        'edit_password.html'
    )


@app.route('/delete/<int:id>')
def delete(id):

    if 'user' not in session:
        return redirect('/')

    db = get_db()

    db.execute(
        "DELETE FROM passwords WHERE id=? AND user=?",
        (id, session['user'])
    )

    db.commit()

    return redirect('/saved-passwords')


@app.route('/change_password', methods=['POST'])
def change_password():

    if 'user' not in session:
        return redirect('/')

    id = request.form['id']

    old = request.form['old_password']

    new = request.form['new_password']

    confirm = request.form['confirm_password']

    db = get_db()

    cur = db.cursor()

    cur.execute(
        "SELECT password FROM passwords WHERE id=? AND user=?",
        (id, session['user'])
    )

    data = cur.fetchone()

    if not data:
        return "Record not found"

    if data[0] != old:
        return "Old password wrong"

    if new != confirm:
        return "Password mismatch"

    cur.execute(
        "UPDATE passwords SET password=? WHERE id=?",
        (new, id)
    )

    db.commit()

    return redirect('/saved-passwords')


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


def init_db():

    db = sqlite3.connect("instance/database.db")

    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        site TEXT,
        username TEXT,
        password TEXT
    )
    """)

    db.commit()

    db.close()


def generate_password(length=12):

    all_chars = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ''.join(
        random.choice(all_chars)
        for _ in range(length)
    )

    return password


def generate_secure_password(length=16):

    all_chars = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ''.join(
        secrets.choice(all_chars)
        for _ in range(length)
    )

    return password


if __name__ == "__main__":

    init_db()

    app.run(debug=True)