from flask import render_template, redirect, url_for, session, Blueprint, request
from mappings.tables import User, db, Route, Business, Location

vlasnik_routes = Blueprint('vlasnik_routes', __name__)

#region Vlasnik routes
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

def vlasnik_update_business(business_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    business = Business.query.get_or_404(business_id)

    if business.ownerid != user_id:
        return "You dont have permission to do that"

    if request.method == 'POST':
        business.businessname = request.form['businessname']
        business.description = request.form['description']
        business.locationid = int(request.form['locationid'])

        db.session.commit()
        return redirect(url_for('vlasnik_show_my_businesses'))

    return render_template('vlasnik_update_business.html', business=business)


def vlasnik_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "VlasnikBiznisa":
            return render_template('vlasnik.html', user=user)
    return redirect(url_for('login'))

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


def vlasnik_delete_business(business_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "VlasnikBiznisa":
            business = Business.query.get(business_id)
            db.session.delete(business)
            db.session.commit()
            return redirect(url_for('vlasnik_show_my_businesses'))
    return redirect(url_for('login'))

def vlasnik_get_business(business_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    business = Business.query.filter_by(businessid=business_id).first()
    if not business:
        return render_template(message='Business not found')

    return render_template('vlasnik_get_business.html', business=business)

def vlasnik_get_route(route_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    route = Route.query.filter_by(routeid=route_id).first()
    if route is None:
        abort(404, description="Route not found")

    if route.public == 'public':
        return render_template('vlasnik_get_route.html', route=route)
    else:
        abort(403, description="You do not have permission to view this route")


#endregion Vlasnik routes