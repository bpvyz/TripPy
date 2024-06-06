from flask import render_template, redirect, url_for, session, Blueprint, request
from mappings.tables import User, db, Route, Business, Location, BusinessRequest, RouteLocation, RouteParticipant
from datetime import datetime, timedelta
from functools import wraps

admin_routes = Blueprint('admin_routes', __name__)

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_id = session['user_id']
        user = User.query.get(user_id)
        if not user or user.usertype != "Administrator":
            return redirect(url_for('login'))

        return func(*args, **kwargs)
    return wrapper

#region Admin routes
@admin_required
def admin_dashboard():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('admin.html', user=user)

@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_required
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('admin_users'))
    else:
        return "User not found", 404

@admin_required
def edit_user(user_id):
    user_to_edit = User.query.get(user_id)
    if user_to_edit:
        return render_template('edit_user.html', user=user_to_edit)
    else:
        return "User not found", 404


@admin_required
def update_user(user_id):
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

@admin_required
def admin_show_businesses():
    businesses = Business.query.join(Location).all()
    return render_template('admin_show_businesses.html', businesses=businesses)

@admin_required
def admin_get_business(business_id):
    business = Business.query.filter_by(businessid=business_id).first()
    if not business:
        return render_template('message_template.html', message='Business not found')

    image_paths = business.image_path.split(',') if business.image_path else []
    return render_template('admin_get_business.html', business=business, image_paths=image_paths)

@admin_required
def admin_delete_business(business_id):
    business = Business.query.get(business_id)
    db.session.delete(business)
    db.session.commit()
    return redirect(url_for('admin_show_businesses'))

@admin_required
def admin_show_routes():
    routes = Route.query.filter((Route.public == 'public')).all()
    return render_template('admin_show_routes.html', routes=routes)

@admin_required
def admin_delete_route(route_id):
    route = Route.query.get(route_id)
    if route is None:
        return "Route not found", 404

    db.session.delete(route)
    db.session.commit()
    return redirect(url_for('admin_show_routes'))

@admin_required
def admin_add_user():
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

@admin_required
def admin_business_requests():
    business_requests = BusinessRequest.query.all()
    return render_template('admin_business_requests.html', business_requests=business_requests)

@admin_required
def admin_approve_business_request(business_request_id):
    business_request = BusinessRequest.query.get(business_request_id)
    if business_request:
        new_business = Business(
            businessname=business_request.businessname,
            description=business_request.description,
            locationid=business_request.locationid,
            ownerid=business_request.ownerid,
            cena=business_request.cena,
            image_path=business_request.image_path,
            currency=business_request.currency
        )
        db.session.add(new_business)
        db.session.delete(business_request)
        db.session.commit()
        return redirect(url_for('admin_business_requests'))
    else:
        return "Business request not found", 404

@admin_required
def admin_delete_business_request(business_request_id):
    business_request = BusinessRequest.query.get(business_request_id)
    if business_request:
        db.session.delete(business_request)
        db.session.commit()
        return redirect(url_for('admin_business_requests'))
    else:
        return "Business request not found", 404

@admin_required
def admin_get_route(route_id):
    route = Route.query.filter_by(routeid=route_id).first()
    if route is None:
        abort(404, description="Route not found")

    route_duration = (route.enddate - route.startdate).days

    if route.public == 'public':
        route_participants = User.query.join(RouteParticipant, User.userid == RouteParticipant.userid).filter(RouteParticipant.routeid == route_id).all()

        return render_template('admin_get_route.html', route=route, route_duration=route_duration, route_participants=route_participants, user_id=session['user_id'])
    else:
        abort(403, description="You do not have permission to view this route")


@admin_required
def admin_show_itinerary(route_id, day_number):
    route = Route.query.get(route_id)
    if not route:
        return "Route not found", 404

    route_duration = (route.enddate - route.startdate).days
    itinerary_details = RouteLocation.query.filter_by(routeid=route_id, day=day_number).all()
    return render_template('itinerary.html', route=route, route_duration=route_duration, day_number=day_number,
                           itinerary_details=itinerary_details, user_id=session['user_id'], user=session['user_type'])

@admin_required
def admin_add_location():
    if request.method == 'POST':
        address = request.form['address']
        new_location = Location(
            address=address,
        )
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_location.html')

#endregion Admin routes
