import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        birthday = request.form['birthday']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not birthday:
            error = 'Birthday is required.'

        

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (email, username, password, birthday) VALUES (?, ?, ?, ?)",
                    (email,username, password, birthday),
                )
                db.commit()
            except db.IntegrityError:
                error = 'db.IntegrityError'
            else:
                return redirect('https://discord.com/app')

        flash(error)

    return render_template('register.html')
@bp.get('/view',)
def view():
    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    return render_template('view.html', users=users)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()
        if user is None:
            error = 'Incorrect email.'
        elif user['password'] != password:
            error = 'Incorrect password.'

        if error is None:
            return redirect('https://discord.com/app')

        flash(error)

    return render_template('login.html')
