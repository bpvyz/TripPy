from flask import render_template, redirect, url_for, session, Blueprint, request
from mappings.tables import User, db, Route, Business, Location

putnik_routes = Blueprint('putnik_routes', __name__)

#region Putnik routes
def putnik_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Putnik":
            return render_template('putnik.html', user=user)
    return redirect(url_for('login'))

def putnik_show_all_routes():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Putnik":
            routes = Route.query.all()
            return render_template('putnik_show_all_routes.html', routes=routes)
    return redirect(url_for('login'))

def putnik_show_my_routes():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Putnik":
            routes = Route.query.filter_by(createdby=user_id).all()
            return render_template('putnik_show_my_routes.html', routes=routes, user_id=user_id)
    return redirect(url_for('login'))

def putnik_show_businesses():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Putnik":
            try:
                businesses = Business.query.all()
                return render_template('putnik_show_businesses.html', businesses=businesses)
            except Exception as e:
                return str(e)
    return redirect(url_for('login'))

def putnik_add_route():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Putnik":
            if request.method == 'POST':
                
                routename = request.form.get('routename')
                description = request.form.get('description')
                startdate = request.form.get('startdate')
                enddate = request.form.get('enddate')
                public = request.form.get('public', 'private') 

          
                new_route = Route(
                    routename=routename,
                    description=description,
                    startdate=startdate,
                    enddate=enddate,
                    createdby=user.userid,
                    public=public
                )
                db.session.add(new_route)
                db.session.commit()
                return redirect(url_for('putnik_dashboard'))
            return render_template('putnik_add_route.html')
    return redirect(url_for('login'))

def putnik_update_route(route_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user or user.usertype != "Putnik":
        return redirect(url_for('login'))

    route = Route.query.get(route_id)
    if not route or route.createdby != user_id:
        return "Route not found or you do not have permission to edit this route", 404

    if request.method == 'POST':
        routename = request.form.get('routename')
        description = request.form.get('description')
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        public = request.form.get('public', 'private')

        route.routename = routename
        route.description = description
        route.startdate = startdate
        route.enddate = enddate
        route.public = public

        db.session.commit()
        return redirect(url_for('putnik_dashboard'))

    return render_template('putnik_update_route.html', route=route)

def putnik_get_business(business_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    business = Business.query.filter_by(businessid=business_id).first()
    if not business:
        return render_template(message='Business not found')

    return render_template('putnik_get_business.html', business=business)

def putnik_get_route(route_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    route = Route.query.filter_by(routeid=route_id).first()
    if route is None:
        return "Route not found", 404

    if route.public == 'public':
        return render_template('putnik_get_route.html', route=route)
    elif 'user_id' in session and session['user_id'] == route.createdby:
        return render_template('putnik_get_route.html', route=route)
    else:
        return "Unauthorized", 403

def putnik_delete_route(route_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    route = Route.query.get(route_id)
    if route is None:
        return "Route not found", 404

    if user.usertype == "Putnik" and route.createdby == user_id:
        db.session.delete(route)
        db.session.commit()
        return redirect(url_for('putnik_show_my_routes'))
    else:
        return "Unauthorized", 403

#endregion Putnik routes