from flask import render_template, redirect, url_for, session, Blueprint, request
from mappings.tables import User, db, Route, Business, Location, BusinessRequest

admin_routes = Blueprint('admin_routes', __name__)

#region Admin routes
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
                        user_to_update.username = request.form.get('username')
                        user_to_update.firstname = request.form.get('firstname')
                        user_to_update.lastname = request.form.get('lastname')
                        user_to_update.email = request.form.get('email')
                        user_to_update.phonenumber = request.form.get('full_phone_number')
                        db.session.commit()
                        return redirect(url_for('admin_users'))
                    else:
                        return "User not found", 404
    return redirect(url_for('login'))

def admin_show_businesses():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            businesses = Business.query.join(Location).all()
            return render_template('admin_show_businesses.html', businesses=businesses)
    return redirect(url_for('login'))

def admin_get_business(business_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    business = Business.query.filter_by(businessid=business_id).first()
    if not business:
        return render_template(message='Business not found')

    return render_template('admin_get_business.html', business=business)


def admin_delete_business(business_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            business = Business.query.get(business_id)
            db.session.delete(business)
            db.session.commit()
            return redirect(url_for('admin_show_businesses'))
    return redirect(url_for('login'))

def admin_show_routes():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            routes = db.session.query(Route, User).join(User, Route.createdby == User.userid).all()
            return render_template('admin_show_routes.html', routes=routes)
    return redirect(url_for('login'))

def admin_delete_route(route_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))
    route = Route.query.get(route_id)
    if route is None:
        return "Route not found", 404

    if user.usertype == "Administrator":
        db.session.delete(route)
        db.session.commit()
        return redirect(url_for('admin_show_routes'))
    else:
        return "Unauthorized", 403



def admin_add_user():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            if request.method == 'POST':
                # Handle form submission
                username = request.form['username']
                password = request.form['password']
                firstname = request.form['first_name']
                lastname = request.form['last_name']
                email = request.form['email']
                phonenumber = request.form['full_phone_number']
                usertype = request.form['user_type']

                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    return render_template('admin_add_user.html', error='Email already exists')

                if User.query.filter_by(username=username).first():
                    return render_template('admin_add_user.html', error='Username already exists')

                new_user = User(
                    username=username,
                    password=password,
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    phonenumber=phonenumber,
                    usertype=usertype
                )
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for('admin_users'))

            return render_template('admin_add_user.html')

    return redirect(url_for('login'))

def admin_business_requests():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            business_requests = BusinessRequest.query.all()
            return render_template('admin_business_requests.html', business_requests=business_requests)
    return redirect(url_for('login'))

def admin_approve_business_request(business_request_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            business_request = BusinessRequest.query.get(business_request_id)
            if business_request:

                new_business = Business(
                    businessname=business_request.businessname,
                    description=business_request.description,
                    locationid=business_request.locationid,
                    ownerid=business_request.ownerid
                )
                db.session.add(new_business)
                db.session.delete(business_request)
                db.session.commit()
                return redirect(url_for('admin_business_requests'))
            else:
                return "Business request not found", 404
    return redirect(url_for('login'))

def admin_delete_business_request(business_request_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            business_request = BusinessRequest.query.get(business_request_id)
            if business_request:
                db.session.delete(business_request)
                db.session.commit()
                return redirect(url_for('admin_business_requests'))
            else:
                return "Business request not found", 404
    return redirect(url_for('login'))

def admin_get_route(route_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    route = Route.query.filter_by(routeid=route_id).first()
    if route is None:
        abort(404, description="Route not found")

    return render_template('admin_get_route.html', route=route)

def admin_add_location():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            if request.method == 'POST':
                address = request.form['address']
                new_location = Location(
                    address=address,
                )
                db.session.add(new_location)
                db.session.commit()
                return redirect(url_for('admin_dashboard'))
            return render_template('admin_add_location.html')
    return redirect(url_for('login'))

#endregion Admin routes
