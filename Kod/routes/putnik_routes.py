from flask import render_template, redirect, url_for, session, Blueprint, request, jsonify
from mappings.tables import User, db, Route, Business, Location, RouteLocation, RouteParticipant
from datetime import datetime, timedelta
from functools import wraps

putnik_routes = Blueprint('putnik_routes', __name__)

def putnik_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_id = session['user_id']
        user = User.query.get(user_id)
        if not user or user.usertype != "Putnik":
            return redirect(url_for('login'))

        return func(*args, **kwargs)
    return wrapper

#region Putnik routes
@putnik_required
def putnik_dashboard():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('putnik.html', user=user)

@putnik_required
def putnik_show_all_routes():
    user_id = session['user_id']
    routes = Route.query.filter((Route.public == 'public') | (Route.createdby == user_id)).all()
    return render_template('putnik_show_all_routes.html', routes=routes)

@putnik_required
def putnik_show_my_routes():
    user_id = session['user_id']
    routes = Route.query.filter_by(createdby=user_id).all()
    return render_template('putnik_show_my_routes.html', routes=routes, user_id=user_id)

@putnik_routes.route('/putnik_show_businesses', methods=['GET'])
@putnik_required
def putnik_show_businesses():
    businesses = Business.query.all()
    return render_template('putnik_show_businesses.html', businesses=businesses)

@putnik_required
def putnik_add_route():
    if request.method == 'POST':
        user_id = session['user_id']
        routename = request.form.get('routename')
        description = request.form.get('description')
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        public = request.form.get('public', 'private')
        participants = request.form.getlist('participants')

        new_route = Route(
            routename=routename,
            description=description,
            startdate=startdate,
            enddate=enddate,
            createdby=user_id,
            public=public
        )
        db.session.add(new_route)
        db.session.flush()  

     
        for participant_id in participants:
            route_participant = RouteParticipant(
                routeid=new_route.routeid,
                userid=participant_id
            )
            db.session.add(route_participant)

        db.session.commit()
        return redirect(url_for('putnik_dashboard'))

   
    users = User.query.all()
    return render_template('putnik_add_route.html', users=users)
    



@putnik_required
def putnik_update_route(route_id):
    route = Route.query.get_or_404(route_id)
    
    if request.method == 'POST':
        route.routename = request.form.get('routename')
        route.description = request.form.get('description')
        route.startdate = request.form.get('startdate')
        route.enddate = request.form.get('enddate')
        route.public = request.form.get('public', 'private')

        # Remove existing participants
        RouteParticipant.query.filter_by(routeid=route_id).delete()

        # Add new participants
        participants = request.form.getlist('participants')
        for participant_id in participants:
            route_participant = RouteParticipant(
                routeid=route.routeid,
                userid=participant_id
            )
            db.session.add(route_participant)
        
        db.session.commit()
        return redirect(url_for('putnik_get_route' , route_id=route.routeid))
    
    # Fetch all users for the participants dropdown
    users = User.query.all()
    # Fetch the current participants
    current_participants = [p.userid for p in route.route_participants]
    
    return render_template('putnik_update_route.html', route=route, users=users, current_participants=current_participants)



@putnik_required
def putnik_get_business(business_id):
    business = Business.query.filter_by(businessid=business_id).first()
    if not business:
        return render_template('message_template.html', message='Business not found')

    image_paths = business.image_path.split(',') if business.image_path else []

    return render_template('putnik_get_business.html', business=business, image_paths=image_paths)


@putnik_required
def putnik_get_route(route_id):
    route = Route.query.filter_by(routeid=route_id).first()
    if route is None:
        return "Route not found", 404

    route_duration = (route.enddate - route.startdate).days

    if route.public == 'public' or route.createdby == session['user_id']:
        route_participants = User.query.join(RouteParticipant, User.userid == RouteParticipant.userid).filter(RouteParticipant.routeid == route_id).all()

        return render_template('putnik_get_route.html', route=route, route_duration=route_duration, route_participants=route_participants, user_id=session['user_id'])
    else:
        return "Unauthorized", 403



@putnik_required
def putnik_delete_route(route_id):
    route = Route.query.get(route_id)
    if route is None:
        return "Route not found", 404

    if route.createdby == session['user_id']:
        db.session.delete(route)
        db.session.commit()
        return redirect(url_for('putnik_show_my_routes'))
    else:
        return "Unauthorized", 403

@putnik_required
def putnik_show_itinerary(route_id, day_number):
    route = Route.query.get(route_id)
    if not route:
        return "Route not found", 404

    route_duration = (route.enddate - route.startdate).days
    itinerary_details = RouteLocation.query.filter_by(routeid=route_id, day=day_number).all()

    return render_template('itinerary.html', route=route, route_duration=route_duration, day_number=day_number,
                           itinerary_details=itinerary_details, user_id=session['user_id'], user=session['user_type'])

@putnik_required
def putnik_add_business(route_id, day_number):
    route = Route.query.get(route_id)
    if route and route.createdby == session['user_id']:
        businesses = Business.query.all()
        return render_template('putnik_add_business.html', businesses=businesses, day=day_number, route_id=route_id)
    return redirect(url_for('login'))

@putnik_required
def putnik_add_business_to_itinerary(route_id, day_number, business_id):
    route = Route.query.get(route_id)
    if route and route.createdby == session['user_id']:
        business = Business.query.get(business_id)
        if not business:
            return "Business not found", 404

        location_id = business.locationid
        route_location = RouteLocation(routeid=route_id, day=day_number, business_id=business_id,
                                                   locationid=location_id)
        db.session.add(route_location)
        db.session.commit()
        return redirect(url_for('putnik_show_itinerary', route_id=route_id, day_number=day_number))

@putnik_required
def putnik_delete_itinerary_business(route_id, day_number, business_id):
    route_location = RouteLocation.query.filter_by(routeid=route_id, day=day_number, business_id=business_id).first()
    if not route_location:
        return "Itinerary detail not found", 404

    db.session.delete(route_location)
    db.session.commit()

    return redirect(url_for('putnik_show_itinerary', route_id=route_id, day_number=day_number))