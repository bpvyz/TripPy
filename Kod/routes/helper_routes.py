import time
from flask import render_template, Blueprint, redirect, url_for, request, session, Blueprint, redirect, flash
from mappings.tables import User, db, Route, Business, Location
from util import generate_verification_code, send_reset_email
import secrets
import string
import os

helper_routes = Blueprint('helper_routes', __name__)

#region Helper routes
def loading():
    return render_template('loading.html')

def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        fullphonenumber = request.form['full_phone_number']
        usertype = request.form['user_type']

        if User.query.filter_by(username=username).first():
            flash('Korisničko ime već postoji. Molimo izaberite drugo korisničko ime.', 'error')
            return redirect(url_for('register'))

        session['registration_data'] = {
            'username': username,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'phonenumber': fullphonenumber,
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
            session['user_type'] = user.usertype
            if user.usertype == "Putnik":
                return redirect(url_for('putnik_dashboard'))
            elif user.usertype == "VlasnikBiznisa":
                return redirect(url_for('vlasnik_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Neispravno korisničko ime ili lozinka!', 'error')  # Flash error message
            return render_template('login.html')

    return render_template('login.html')


def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def settings():
    if 'user_id' in session:
        user = session['user_type']
        return render_template('settings.html', dark_mode=session.get('dark_mode', False), user=user)
    else:
        return redirect(url_for('login'))

def toggle_theme():
    if request.method == 'POST':
        # pribavlja se vrednost checkbox-a za dark mode i proverava se da li je stikliran:
        dark_mode = request.form.get('darkMode') == 'on'

        # ubacuje se u sesiju u promenljivu 'dark_mode'
        session['dark_mode'] = dark_mode

        #redirect nazad na dashboard odgovarajuceg korisnika
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
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if request.method == 'POST':
            user.username = request.form.get('username')
            new_password = request.form.get('newPassword')
            if new_password:
                user.password = new_password
            user.email = request.form.get('email')
            user.phonenumber = request.form.get('full_phone_number')
            user.firstname = request.form.get('firstname')
            user.lastname = request.form.get('lastname')

            upload_dir = os.path.join(os.getcwd(), 'static', 'uploads')
            if 'profile_picture' in request.files:
                
                file = request.files['profile_picture']
                if file.filename != '':
                    filename = file.filename
                    file_path = os.path.join(upload_dir, filename)
                    rel_path = os.path.join('/static/uploads', filename).replace('\\', '/')
                    file.save(file_path)
                    user.profilna = rel_path 

            db.session.commit()
            flash('Profile updated successfully!', 'success')

            if user.usertype == "Putnik":
                return redirect(url_for('putnik_dashboard'))
            elif user.usertype == "VlasnikBiznisa":
                return redirect(url_for('vlasnik_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))

        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
            reset_tokens[email] = token
            send_reset_email(email, token)
            flash('Reset link sent to your email.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email not found.', 'error')
    return render_template('forgot_password.html')

reset_tokens = {}
def reset_password(token):
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', token=token)

        if token in reset_tokens.values():
            email = [email for email, t in reset_tokens.items() if t == token][0]
            user = User.query.filter_by(email=email).first()
            user.password = password
            db.session.commit()
            flash('Password reset successfully.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired token.', 'error')
            return redirect(url_for('forgot_password'))
    if token in reset_tokens.values():
        return render_template('reset_password.html', token=token)
    else:
        flash('Invalid or expired token.', 'error')
        return redirect(url_for('forgot_password'))
