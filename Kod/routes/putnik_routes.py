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
                routename = request.form['routename']
                description = request.form['description']
                startdate = request.form['startdate']
                enddate = request.form['enddate']

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

def putnik_get_business(business_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    business = Business.query.filter_by(businessid=business_id).first()
    if not business:
        return render_template(message='Business not found')

    return render_template('putnik_get_business.html', business=business)

#endregion Putnik routes