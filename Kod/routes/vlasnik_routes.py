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
#endregion Vlasnik routes