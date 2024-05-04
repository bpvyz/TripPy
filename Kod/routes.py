from flask import render_template, redirect, url_for, request, session
from mappings.tables import User, db

def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        user_type = request.form['user_type']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')

        new_user = User(
            username=username,
            password=password,
            usertype=user_type,
            firstname=first_name,
            lastname=last_name,
            email=email,
            phonenumber=phone_number
        )

        db.session.add(new_user)

        try:
            db.session.commit()
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            return render_template('register.html', error='An error occurred while registering')

    return render_template('register.html')

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.userid
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('login'))

def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

