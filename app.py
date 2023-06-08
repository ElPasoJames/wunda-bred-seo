import requests
from flask import Flask, flash, redirect, render_template, session, request
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError

from inspect import getmembers
from pprint import pprint

cred = credentials.Certificate('json/fbAdminConfig.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = 'gpt-secret-key'

API_KEY = 'AIzaSyCLEPrZxeYkN73c5vAb-BBqdn2dVAxyJ0Q'
AUTH_API_BASE_URL = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate the user's email and password with Firebase
        response = requests.post(f'{AUTH_API_BASE_URL}', json={
            'email': email,
            'password': password,
            'returnSecureToken': True
        })

        if response.ok:
            # Store the Firebase ID token in a session variable or cookie
            session['user'] = response.json()['localId']

            # Redirect to a protected page that requires authentication
            return redirect('/')
        else:
            # Handle any errors that occur during authentication
            # error_message = response.json().get('error', {}).get('message', 'Invalid email or password.')
            error_message = 'Invalid email or password.'
            flash(error_message)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user(
                email=email,
                password=password,
            )
            session['user'] = user.uid
            flash('Registered successfully!', 'success')
            return redirect('/')
        except FirebaseError as e:
            error = str(e)
            flash(error, 'error')

    return render_template('register.html')

if __name__ == '__main__':
    # The port our Flask app will run on
    app.run(debug=True, port=6100)
