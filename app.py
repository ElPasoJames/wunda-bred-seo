import os
from flask import Flask, render_template, request
from firebase_admin import auth, credentials, initialize_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.get_user_by_email(email)
            auth.sign_in_with_email_and_password(email, password)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        except:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            flash('Registered successfully!', 'success')
            return redirect(url_for('dashboard'))
        except:
            flash('Registration failed', 'error')

    return render_template('register.html')

if __name__ == '__main__':
    # The port our Flask app will run on
    app.run(debug=True, port=6100)
