# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
import datetime
import pymysql
from sqlalchemy import create_engine
# from werkzeug.security import check_password_hash, generate_password_hash

from flask import (Flask, render_template, sessions, flash, request, redirect, url_for)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

# Connect to the database
unix_socket = '/cloudsql/{}'.format('hackmit2019-252916:us-central1:hackmit2019')
connection = pymysql.connect(user='root',
                             password='root',
                             db='hackmit',
                             unix_socket=unix_socket,
                             charset='utf8mb4',
                             #cursorclass=pymysql.cursors.DictCursor
                             )

@app.route('/signup', methods=('GET', 'POST'))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        first = request.form['first']
        last = request.form['last']
        email = request.form['email']
        pwd_not_hash = request.form['password']
        
        error = None

        if not first:
            error = 'First name is required.'
        elif not last:
            error = 'Last name is required.'
        elif not email:
            error = 'Email is required.'
        elif not pwd_not_hash:
            error = 'Password is required.'
          
        elif connection.cursor().execute("SELECT `id` FROM `user_table` WHERE `email`=%s", (email,)) == "0":
            error = 'User {0} is already registered.'.format(email)
            print(connection.cursor().execute("SELECT `id` FROM `user_table` WHERE `email`=%s", (email,)))

        if error is None:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `user_table` (`first_name`, `last_name`, `email`, `password`) VALUES (%s, %s, %s, %s)"
                print('past sql')
                cursor.execute(sql, (first, last, email, pwd_not_hash))
                print('past execute')
            connection.commit()
            print("I did things!")
        else:
            print("error is not none")
            print(error)
        flash(error)
        #return redirect(url_for('index.html'))

    print('about to render something')
    return render_template('signup.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = connection.cursor.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        )

        if user == "0":
            error = 'Incorrect email.'
        elif user['password'] != password:
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/homepage')
def home():
    return render_template('homepage.html')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    # app.secret_key = 'dev'
    # app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)

    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
