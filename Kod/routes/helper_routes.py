from flask import render_template, Blueprint, redirect, url_for, request, session, Blueprint, redirect
from mappings.tables import User, db, Route, Business, Location
from util import generate_verification_code
import secrets
import string

helper_routes = Blueprint('helper_routes', __name__)

#region Helper routes
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        phonenumber = request.form['phone_number']
        usertype = request.form['user_type']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')

        session['registration_data'] = {
            'username': username,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'phonenumber': phonenumber,
            'usertype': usertype
        }

        verification_code = generate_verification_code()
        session['expected_verification_code'] = verification_code

        return redirect(url_for('verify'))

    else:
        return render_template('register.html')

def verify():
    if request.method == 'POST':
        verification_code = request.form['verification_code']

        expected_verification_code = session.get('expected_verification_code')

        if verification_code == expected_verification_code:
            registration_data = session.get('registration_data', {})
            new_user = User(username=registration_data['username'], password=registration_data['password'],
                            firstname=registration_data['firstname'], lastname=registration_data['lastname'],
                            email=registration_data['email'], phonenumber=registration_data['phonenumber'],
                            usertype=registration_data['usertype'])
            db.session.add(new_user)
            db.session.commit()

            session.pop('expected_verification_code', None)
            session.pop('registration_data', None)

            return render_template('redirect_login.html')
        else:
            error = "Verification code incorrect. Please try again."
            return render_template('verification_code.html', error=error)

    expected_verification_code = session.get('expected_verification_code')
    registration_data = session.get('registration_data', {})

    if expected_verification_code:
        return render_template('verification_code.html', expected_verification_code=expected_verification_code, registration_data=registration_data)
    else:
        return redirect(url_for('register'))

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.userid
            if user.usertype == "Putnik":
                return redirect(url_for('putnik_dashboard'))
            elif user.usertype == "VlasnikBiznisa":
                return redirect(url_for('vlasnik_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def settings():
    if 'user_id' in session:
        return render_template('settings.html', dark_mode=session.get('dark_mode', False))
    else:
        return redirect(url_for('login'))

def toggle_theme():
    if request.method == 'POST':
        dark_mode = request.form.get('darkMode') == 'on'

        session['dark_mode'] = dark_mode
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user.usertype == "Putnik":
                return redirect(url_for('putnik_dashboard'))
            elif user.usertype == "VlasnikBiznisa":
                return redirect(url_for('vlasnik_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
        return render_template('login.html')
    return render_template('login.html')