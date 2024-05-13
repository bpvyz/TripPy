from flask import render_template, redirect, url_for, session, Blueprint, request, jsonify
from mappings.tables import User, db, Route, Business, Location, BusinessRequest
import os

vlasnik_routes = Blueprint('vlasnik_routes', __name__)

#region Vlasnik routes
def autocomplete_locations():
    term = request.args.get('term', '')

    locations = Location.query.filter(Location.address.ilike(f'%{term}%')).all()

    suggestions = [{'id': location.locationid, 'label': location.address, 'value': f"{location.address}"}
                   for location in locations]

    return jsonify(suggestions)


def vlasnik_add_business_request():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        businessname = request.form['businessname']
        description = request.form['description']
        locationid = request.form['locationid']
        cena = request.form['cena']
        user_id = session.get('user_id')

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
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "VlasnikBiznisa":
            routes = Route.query.filter((Route.public == 'public')).all()
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
        return render_template('message_template.html', message='Business not found') 

    image_paths = business.image_path.split(',') if business.image_path else []
    return render_template('vlasnik_get_business.html', business=business, image_paths=image_paths)

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