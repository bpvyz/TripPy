from flask import render_template, redirect, url_for, session, Blueprint, request, jsonify
from functools import wraps
from mappings.tables import User, db, Route, Business, Location, BusinessRequest, RouteLocation
import os
import time

vlasnik_routes = Blueprint('vlasnik_routes', __name__)

def vlasnik_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype != "VlasnikBiznisa":
            return redirect(url_for('login'))

        return func(*args, **kwargs)
    return wrapper

#region Vlasnik routes

@vlasnik_required
def autocomplete_locations():
    term = request.args.get('term', '')

    locations = Location.query.filter(Location.address.ilike(f'%{term}%')).all()

    suggestions = [{'id': location.locationid, 'label': location.address, 'value': f"{location.address}"}
                   for location in locations]

    if not suggestions and term:
        suggestions.append({'id': -1, 'label': f"Add new location: '{term}'", 'value': term})

    return jsonify(suggestions)

@vlasnik_required
def vlasnik_add_business_request():
    if request.method == 'POST':
        businessname = request.form['businessname']
        description = request.form['description']
        location_name = request.form['location']
        cena = request.form['cena']
        user_id = session.get('user_id')

        location = Location.query.filter_by(address=location_name).first()
        if not location:
            location = Location(address=location_name)
            db.session.add(location)
            db.session.commit()

        locationid = location.locationid

        images = request.files.getlist('images')
        image_paths = []

        upload_dir = os.path.join(os.getcwd(), 'static', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        for image in images:
            if image and '.' in image.filename:
                filename = image.filename
                image_path = os.path.join(upload_dir, filename)
                image.save(image_path)
                rel_path = os.path.join('uploads', filename).replace('\\', '/')
                image_paths.append(rel_path)

        image_paths_string = ','.join(image_paths)

        if user_id:
            user = User.query.get(user_id)
            if user:
                new_business_request = BusinessRequest(
                    businessname=businessname,
                    description=description,
                    locationid=locationid,
                    ownerid=user.userid,
                    cena=cena,
                    image_path=image_paths_string
                )
                db.session.add(new_business_request)
                db.session.commit()
                return redirect(url_for('vlasnik_dashboard'))

    return render_template('vlasnik_add_business.html')

@vlasnik_required
def vlasnik_dashboard():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('vlasnik.html', user=user)

@vlasnik_required
def vlasnik_show_all_businesses():
    try:
        businesses = Business.query.all()
        return render_template('vlasnik_show_all_businesses.html', businesses=businesses)
    except Exception as e:
        return str(e)

@vlasnik_required
def vlasnik_show_my_businesses():
    user_id = session['user_id']
    businesses = Business.query.filter_by(ownerid=user_id).all()
    return render_template('vlasnik_show_my_businesses.html', businesses=businesses, user_id=user_id)

@vlasnik_required
def vlasnik_show_routes():
    routes = Route.query.filter((Route.public == 'public')).all()
    return render_template('vlasnik_show_routes.html', routes=routes)

@vlasnik_required
def vlasnik_delete_business(business_id):
    business = Business.query.get(business_id)
    db.session.delete(business)
    db.session.commit()
    return redirect(url_for('vlasnik_show_my_businesses'))

@vlasnik_required
def vlasnik_get_business(business_id):
    business = Business.query.filter_by(businessid=business_id).first()
    user_id = session['user_id']
    if not business:
        return render_template('message_template.html', message='Business not found')
    image_paths = business.image_path.split(',') if business.image_path else []
    return render_template('vlasnik_get_business.html', business=business, image_paths=image_paths, user_id=user_id)

@vlasnik_required
def vlasnik_get_route(route_id):
    route = Route.query.filter_by(routeid=route_id).first()
    if route is None:
        abort(404, description="Route not found")

    route_duration = (route.enddate - route.startdate).days

    if route.public == 'public':
        return render_template('vlasnik_get_route.html', route=route, route_duration=route_duration)
    else:
        abort(403, description="You do not have permission to view this route")

@vlasnik_required
def vlasnik_show_itinerary(route_id, day_number):
    route = Route.query.get(route_id)
    if not route:
        return "Route not found", 404

    route_duration = (route.enddate - route.startdate).days
    itinerary_details = RouteLocation.query.filter_by(routeid=route_id, day=day_number).all()
    return render_template('itinerary.html', route=route, route_duration=route_duration, day_number=day_number,
                           itinerary_details=itinerary_details, user_id=session['user_id'], user=session['user_type'])

@vlasnik_required
def vlasnik_edit_business(business_id):
    business = Business.query.get_or_404(business_id)
    if business.ownerid != session['user_id']:
        return "You don't have permission to do that"

    if request.method == 'POST':
        business.businessname = request.form['businessname']
        business.description = request.form['description']

        location_id = request.form['locationid']

        if location_id == '-1':
            location_address = request.form['location']
            new_location = Location(address=location_address)
            db.session.add(new_location)
            db.session.flush()
            location_id = new_location.locationid
        else:
            location = Location.query.get(location_id)
            if not location:
                location_address = request.form['location']
                new_location = Location(locationid=location_id, address=location_address)
                db.session.add(new_location)
                db.session.flush()

        business.locationid = location_id

        removed_images = request.form.getlist('removed_images')
        if removed_images:
            current_images = business.image_path.split(',')
            updated_images = [img for img in current_images if img not in removed_images]
            business.image_path = ','.join(updated_images)
            for img in removed_images:
                image_path = os.path.join(os.getcwd(), 'static', img.strip('/'))
                if os.path.exists(image_path):
                    os.remove(image_path)

        images = request.files.getlist('images[]')
        if images:
            upload_dir = os.path.join(os.getcwd(), 'static', 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            for image in images:
                if image and '.' in image.filename:
                    filename = image.filename
                    image_path = os.path.join(upload_dir, filename)
                    image.save(image_path)
                    rel_path = os.path.join('uploads', filename).replace('\\', '/')
                    business.image_path = f"{business.image_path},{rel_path}" if business.image_path else rel_path

        db.session.commit()
        return redirect(url_for('vlasnik_show_my_businesses'))

    image_paths = business.image_path.split(',') if business.image_path else []
    return render_template('vlasnik_edit_business.html', business=business, image_paths=image_paths)
#endregion Vlasnik routes