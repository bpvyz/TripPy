from init import create_app

from routes.helper_routes import *
from routes.admin_routes import *
from routes.putnik_routes import *
from routes.vlasnik_routes import *

app = create_app()

app.register_blueprint(helper_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(putnik_routes)
app.register_blueprint(vlasnik_routes)

# Routes
app.add_url_rule('/', 'login', login)
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/verify', 'verify', verify, methods=['GET', 'POST'])
app.add_url_rule('/settings', 'settings', settings, methods=['GET', 'POST'])
app.add_url_rule('/toggle_theme', 'toggle_theme', toggle_theme, methods=['GET', 'POST'])
app.add_url_rule('/putnik_dashboard', 'putnik_dashboard', putnik_dashboard, methods=['GET', 'POST'])
app.add_url_rule('/vlasnik_dashboard', 'vlasnik_dashboard', vlasnik_dashboard, methods=['GET', 'POST'])
app.add_url_rule('/admin_dashboard', 'admin_dashboard', admin_dashboard, methods=['GET', 'POST'])
app.add_url_rule('/putnik_add_route', 'putnik_add_route', putnik_add_route, methods=['GET', 'POST'])
app.add_url_rule('/putnik_update_route/<int:route_id>', 'putnik_update_route', putnik_update_route, methods=['GET', 'POST'])
app.add_url_rule('/putnik_show_all_routes', 'putnik_show_all_routes', putnik_show_all_routes, methods=['GET'])
app.add_url_rule('/putnik_get_route/<int:route_id>', 'putnik_get_route', putnik_get_route, methods=['GET'])
app.add_url_rule('/putnik_delete_route/<int:route_id>', 'putnik_delete_route', putnik_delete_route, methods=['GET', 'DELETE'])
app.add_url_rule('/putnik_show_my_routes', 'putnik_show_my_routes', putnik_show_my_routes, methods=['GET'])
app.add_url_rule('/putnik_show_businesses', 'putnik_show_businesses', putnik_show_businesses, methods=['GET'])
app.add_url_rule('/putnik_get_business/<int:business_id>', 'putnik_get_business', putnik_get_business, methods=['GET'])
app.add_url_rule('/admin_users', 'admin_users', admin_users, methods=['GET', 'POST'])
app.add_url_rule('/admin_add_user', 'admin_add_user', admin_add_user, methods = ['GET', 'POST'])
app.add_url_rule('/delete_user/<int:user_id>', 'delete_user', delete_user, methods=['POST'])
app.add_url_rule('/edit_user/<int:user_id>', 'edit_user', edit_user, methods=['GET'])
app.add_url_rule('/update_user/<int:user_id>', 'update_user', update_user, methods=['POST'])
app.add_url_rule('/admin_show_businesses', 'admin_show_businesses', admin_show_businesses, methods=['POST', 'GET'])
app.add_url_rule('/admin_get_business/<int:business_id>', 'admin_get_business', admin_get_business, methods=['GET'])
app.add_url_rule('/admin_delete_business/<int:business_id>', 'admin_delete_business', admin_delete_business, methods=['POST', 'GET'])
app.add_url_rule('/admin_show_routes', 'admin_show_routes', admin_show_routes, methods=['GET'])
app.add_url_rule('/admin_get_route/<int:route_id>', 'admin_get_route', admin_get_route, methods=['GET'])
app.add_url_rule('/admin_delete_route/<int:route_id>', 'admin_delete_route', admin_delete_route, methods=['GET', 'DELETE'])
app.add_url_rule('/admin_business_requests', 'admin_business_requests', admin_business_requests, methods=['GET', 'POST'])
app.add_url_rule('/admin_approve_business_request/<int:business_request_id>', 'admin_approve_business_request', admin_approve_business_request, methods=['GET', 'POST'])
app.add_url_rule('/admin_delete_business_request/<int:business_request_id>', 'admin_delete_business_request', admin_delete_business_request, methods=['GET', 'POST'])
app.add_url_rule('/admin_add_location', 'admin_add_location', admin_add_location, methods=['GET', 'POST'])
app.add_url_rule('/vlasnik_add_business', 'vlasnik_add_business', vlasnik_add_business_request, methods=['GET', 'POST'])
app.add_url_rule('/vlasnik_update_business/<int:business_id>', 'vlasnik_update_business', vlasnik_update_business, methods=['POST', 'GET'])
app.add_url_rule('/vlasnik_show_all_businesses', 'vlasnik_show_all_businesses', vlasnik_show_all_businesses, methods=['GET'])
app.add_url_rule('/vlasnik_show_my_businesses', 'vlasnik_show_my_businesses', vlasnik_show_my_businesses, methods=['GET'])
app.add_url_rule('/vlasnik_show_routes', 'vlasnik_show_routes', vlasnik_show_routes, methods=['GET'])
app.add_url_rule('/vlasnik_delete_business/<int:business_id>', 'vlasnik_delete_business', vlasnik_delete_business, methods=['POST', 'GET'])
app.add_url_rule('/vlasnik_get_business/<int:business_id>', 'vlasnik_get_business', vlasnik_get_business, methods=['GET'])
app.add_url_rule('/autocomplete_locations', 'autocomplete_locations', autocomplete_locations, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
