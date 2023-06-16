
import os
import requests
from flask import Flask, flash, redirect, render_template, session, request, url_for
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError
import core

current_folder = os.path.dirname(os.path.abspath(__file__))
file_name = current_folder + "/json/fbAdminConfig.json"
cred = credentials.Certificate(file_name)
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = 'gpt-secret-key'

API_KEY = 'xxxxxxxxxx'
AUTH_API_BASE_URL = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        input3 = request.form['input3']
        inputs = [input1, input2, input3]
        result = core.process_gpt(inputs)

        flash(result)

    return render_template('dashboard.html')

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
            session['logged_in'] = True

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
            auth.create_user(
                email=email,
                password=password,
            )
            # session['user'] = user.uid
            session['logged_in'] = True

            flash('Registered successfully!', 'success')
            return redirect('/')
        except FirebaseError as e:
            error = str(e)
            flash(error, 'error')

            # Pass the error message to the template
            return render_template('register.html', error=error)

    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear the session data and log the user out of Firebase
    session.pop('logged_in', None)
    # auth.revoke_refresh_tokens(session['user'])
    return redirect('/')    

if __name__ == '__main__':
    app.run(debug=True)


