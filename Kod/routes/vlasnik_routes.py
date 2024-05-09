from flask import render_template, redirect, url_for, session, Blueprint, request, jsonify
from mappings.tables import User, db, Route, Business, Location, BusinessRequest

vlasnik_routes = Blueprint('vlasnik_routes', __name__)

#region Vlasnik routes
def autocomplete_locations():
    term = request.args.get('term', '')

    locations = Location.query.filter(Location.address.ilike(f'%{term}%')).all()

    suggestions = [{'id': location.locationid, 'label': location.address, 'value': f"{location.address}"}
                   for location in locations]

    return jsonify(suggestions)


def vlasnik_add_business_request():
    if 'user_id' in session:
        if request.method == 'POST':
            businessname = request.form['businessname']
            description = request.form['description']
            locationid = request.form['locationid']
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
                if user:
                    new_business_request = BusinessRequest(
                        businessname=businessname,
                        description=description,
                        locationid=int(locationid),
                        ownerid=user.userid
                    )
                    db.session.add(new_business_request)
                    db.session.commit()
                    return redirect(url_for('vlasnik_dashboard'))

        return render_template('vlasnik_add_business.html')
    return redirect(url_for('login'))

   

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


#endregion Vlasnik routes