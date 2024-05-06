from flask import render_template, redirect, url_for, request, session
from mappings.tables import User, db, Route, Business, Location, Route
import secrets
import string

import string
import secrets

def generate_verification_code():
    alphabet = string.ascii_letters + string.digits
    verification_code = ''.join(secrets.choice(alphabet) for _ in range(6))
    print(f"Verification code: {verification_code}")
    return verification_code

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

from flask import redirect, url_for, session

def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def admin_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            return render_template('admin.html', user=user)
    return redirect(url_for('login'))

def admin_users():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            users = User.query.all()
            return render_template('admin_users.html', users=users)
    return redirect(url_for('login'))

def delete_user(user_id):
    if 'user_id' in session:
        logged_in_user_id = session['user_id']
        user = User.query.get(logged_in_user_id)
        if user and user.usertype == "Administrator":
            user_to_delete = User.query.get(user_id)
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                return redirect(url_for('admin_users'))
            else:
                return "User not found", 404
    return redirect(url_for('login'))

def edit_user(user_id):
    if 'user_id' in session:
        logged_in_user_id = session['user_id']
        user = User.query.get(logged_in_user_id)
        if user:
            if user.usertype == "Administrator" or user.userid == user_id:
                user_to_edit = User.query.get(user_id)
                if user_to_edit:
                    return render_template('edit_user.html', user=user_to_edit)
                else:
                    return "User not found", 404
    return redirect(url_for('login'))

def update_user(user_id):
    if request.method == 'POST':
        if 'user_id' in session:
            logged_in_user_id = session['user_id']
            user = User.query.get(logged_in_user_id)
            if user:
                if user.usertype == "Administrator" or user.userid == user_id:
                    user_to_update = User.query.get(user_id)
                    if user_to_update:
                        return redirect(url_for('admin_users'))
                    else:
                        return "User not found", 404
    return redirect(url_for('login'))

def putnik_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Putnik":
            return render_template('putnik.html', user=user)
    return redirect(url_for('login'))

def vlasnik_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "VlasnikBiznisa":
            return render_template('vlasnik.html', user=user)
    return redirect(url_for('login'))

def putnik_show_all_routes():
    if 'user_id' in session:

        routes = Route.query.all()
        return render_template('putnik_show_all_routes.html', routes=routes)
    return redirect(url_for('login'))

def putnik_show_my_routes():
    if 'user_id' in session:
        user_id = session['user_id']
        routes = Route.query.filter_by(createdby=user_id).all()
        return render_template('putnik_show_my_routes.html', routes=routes, user_id=user_id)
    return redirect(url_for('login'))

def putnik_show_businesses():
    if 'user_id' in session:
        try:
            businesses = Business.query.all()
            return render_template('putnik_show_businesses.html', businesses=businesses)
        except Exception as e:
            return str(e)
    return redirect(url_for('login'))

def putnik_add_route():
    if 'user_id' in session:
        if request.method == 'POST':
            routename = request.form['routename']
            description = request.form['description']
            startdate = request.form['startdate']
            enddate = request.form['enddate']

            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
                if user:

                    new_route = Route(
                        routename=routename,
                        description=description,
                        startdate=startdate,
                        enddate=enddate,
                        createdby=user.userid
                    )
                    db.session.add(new_route)
                    db.session.commit()
                    return redirect(url_for('putnik_dashboard'))

        return render_template('putnik_add_route.html')
    return redirect(url_for('login'))

def vlasnik_add_business():
    if 'user_id' in session:
        if request.method == 'POST':
            businessname = request.form['businessname']
            description = request.form['description']
            locationid = request.form['locationid']
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
                if user:

                    new_business = Business(
                        businessname=businessname,
                        description=description,
                        locationid=int(locationid),
                        ownerid=user.userid
                    )
                    db.session.add(new_business)
                    db.session.commit()
                    return redirect(url_for('vlasnik_dashboard'))

        return render_template('vlasnik_add_business.html')
    return redirect(url_for('login'))

    return render_template('add_route.html')

def admin_show_businesses():
    businesses = Business.query.join(Location).all()
    return render_template('admin_show_businesses.html', businesses=businesses)

def admin_delete_business(business_id):
    business = Business.query.get(business_id)
    db.session.delete(business)
    db.session.commit()
    return redirect('/admin_show_businesses')

def admin_show_routes():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            routes = db.session.query(Route, User).join(User, Route.createdby == User.userid).all()
            return render_template('admin_show_routes.html', routes=routes)
    return redirect(url_for('login'))

def admin_delete_route(route_id):
    if request.method == 'POST':
        route = Route.query.get(route_id)
        if route:
            db.session.delete(route)
            db.session.commit()
    return redirect(url_for('admin_show_routes'))

def vlasnik_show_all_businesses():
    if 'user_id' in session:
        try:
            businesses = Business.query.all()
            return render_template('vlasnik_show_all_businesses.html', businesses=businesses)
        except Exception as e:
            return str(e)
    return redirect(url_for('login'))

def vlasnik_show_my_businesses():
    if 'user_id' in session:
        user_id = session['user_id']
        businesses = Business.query.filter_by(ownerid=user_id).all()
        return render_template('vlasnik_show_my_businesses.html', businesses=businesses, user_id=user_id)
    return redirect(url_for('login'))

def vlasnik_show_routes():
    if 'user_id' in session:

        routes = Route.query.all()
        return render_template('vlasnik_show_routes.html', routes=routes)
    return redirect(url_for('login'))
