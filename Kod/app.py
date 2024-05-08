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
app.add_url_rule('/putnik_dashboard', 'putnik_dashboard', putnik_dashboard, methods=['GET', 'POST'])
app.add_url_rule('/vlasnik_dashboard', 'vlasnik_dashboard', vlasnik_dashboard, methods=['GET', 'POST'])
app.add_url_rule('/admin_dashboard', 'admin_dashboard', admin_dashboard, methods=['GET', 'POST'])
app.add_url_rule('/putnik_add_route', 'putnik_add_route', putnik_add_route, methods=['GET', 'POST'])
app.add_url_rule('/putnik_show_all_routes', 'putnik_show_all_routes', putnik_show_all_routes, methods=['GET'])
app.add_url_rule('/putnik_show_my_routes', 'putnik_show_my_routes', putnik_show_my_routes, methods=['GET'])
app.add_url_rule('/putnik_show_businesses', 'putnik_show_businesses', putnik_show_businesses, methods=['GET'])
app.add_url_rule('/admin_users', 'admin_users', admin_users, methods=['GET', 'POST'])
app.add_url_rule('/admin_add_user', 'admin_add_user', admin_add_user, methods = ['GET', 'POST'])
app.add_url_rule('/delete_user/<int:user_id>', 'delete_user', delete_user, methods=['POST'])
app.add_url_rule('/edit_user/<int:user_id>', 'edit_user', edit_user, methods=['GET'])
app.add_url_rule('/update_user/<int:user_id>', 'update_user', update_user, methods=['POST'])
app.add_url_rule('/admin_show_businesses', 'admin_show_businesses', admin_show_businesses, methods=['POST', 'GET'])
app.add_url_rule('/admin_delete_business/<int:business_id>', 'admin_delete_business', admin_delete_business, methods=['POST'])
app.add_url_rule('/admin_show_routes', 'admin_show_routes', admin_show_routes, methods=['GET'])
app.add_url_rule('/admin_delete_route/<int:route_id>', 'admin_delete_route', admin_delete_route, methods=['POST'])
app.add_url_rule('/vlasnik_add_business', 'vlasnik_add_business', vlasnik_add_business, methods=['POST', 'GET'])
app.add_url_rule('/vlasnik_show_all_businesses', 'vlasnik_show_all_businesses', vlasnik_show_all_businesses, methods=['GET'])
app.add_url_rule('/vlasnik_show_my_businesses', 'vlasnik_show_my_businesses', vlasnik_show_my_businesses, methods=['GET'])
app.add_url_rule('/vlasnik_show_routes', 'vlasnik_show_routes', vlasnik_show_routes, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
