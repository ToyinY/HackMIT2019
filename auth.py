# import functools
# import pymysql.cursors
# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from werkzeug.security import check_password_hash, generate_password_hash

# connection = pymysql.connect(host='35.202.234.225',
#                              user='root',
#                              password='root',
#                              db='hackmit',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# bp = Blueprint('auth', __name__, url_prefix='/auth')

# def login_required(view):
#     """View decorator that redirects anonymous users to the login page."""
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view


# @bp.before_app_request
# def load_logged_in_user():
#     """If a user id is stored in the session, load the user object from
#     the database into ``g.user``."""
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = connection.execute(
#             'SELECT * FROM user WHERE idUser = ?', (user_id,)
#         ).fetchone()


# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     """Register a new user.
#     Validates that the username is not already taken. Hashes the
#     password for security.
#     """
#     if request.method == 'POST':
#         first = request.form['first']
#         last = request.form['last']
#         email = request.form['email']
#         pwd_not_hash = request.form['password']
        
#         error = None

#         if not first:
#             error = 'First name is required.'
#         elif not last:
#             error = 'Last name is required.'
#         elif not email:
#             error = 'Email is required.'
#         elif not pwd_not_hash:
#             error = 'Password is required.'
#         elif connection.execute(
#             'SELECT idUser FROM user WHERE email = ?', (email,)
#         ) is not None:
#             error = 'User {0} is already registered.'.format(email)

#         if error is None:
#             # the name is available, store it in the database and go to
#             # the login page
#             with connection.cursor() as cursor:
#             # Create a new record
#             sql = "INSERT INTO `users` (`first_name`, `last_name`, `email`, `password`) VALUES (%s, %s, %s, %s)"
#             cursor.execute(sql, (first, last, email, generate_password_hash(pwd_not_hash)))

#         flash(error)
#         return render_template('register.html')

# @bp.route('/login', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         error = None
#         user = connection.execute(
#             'SELECT * FROM user WHERE email = ?', (email,)
#         )

#         if user is None:
#             error = 'Incorrect email.'
#         elif not check_password_hash(user['password'], password):
#             error = 'Incorrect password.'

#         if error is None:
#             # store the user id in a new session and return to the index
#             session.clear()
#             session['user_id'] = user['idUser']
#             return redirect(url_for('index'))

#         flash(error)

#     return render_template('login.html')


# @bp.route('/logout')
# def logout():
#     """Clear the current session, including the stored user id."""
#     session.clear()
#     return redirect(url_for('index'))