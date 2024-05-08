from flask import render_template, redirect, url_for, session, Blueprint
from mappings.tables import User, db, Route, Business, Location

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
                        return redirect(url_for('admin_users'))
                    else:
                        return "User not found", 404
    return redirect(url_for('login'))

def admin_show_businesses():
    businesses = Business.query.join(Location).all()
    return render_template('admin_show_businesses.html', businesses=businesses)

def admin_delete_business(business_id):
    business = Business.query.get(business_id)
    db.session.delete(business)
    db.session.commit()
    return redirect('/admin_show_businesses')

def admin_show_routes():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.usertype == "Administrator":
            routes = db.session.query(Route, User).join(User, Route.createdby == User.userid).all()
            return render_template('admin_show_routes.html', routes=routes)
    return redirect(url_for('login'))

def admin_delete_route(route_id):
    if request.method == 'POST':
        route = Route.query.get(route_id)
        if route:
            db.session.delete(route)
            db.session.commit()
    return redirect(url_for('admin_show_routes'))
#endregion Admin routes