from init import create_app
from routes import login, logout, register, verify, putnik_dashboard, vlasnik_dashboard, admin_dashboard, admin_users, delete_user, edit_user, update_user , putnik_show_all_routes, putnik_show_my_routes, putnik_show_businesses, vlasnik_add_business, vlasnik_show_all_businesses, vlasnik_show_my_businesses, vlasnik_show_routes

app = create_app()

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
app.add_url_rule('/delete_user/<int:user_id>', 'delete_user', delete_user, methods=['POST'])
app.add_url_rule('/edit_user/<int:user_id>', 'edit_user', edit_user, methods=['GET'])
app.add_url_rule('/update_user/<int:user_id>', 'update_user', update_user, methods=['POST'])
app.add_url_rule('/vlasnik_add_business', 'vlasnik_add_business', vlasnik_add_business, methods=['GET', 'POST'])
app.add_url_rule('/vlasnik_show_all_businesses', 'vlasnik_show_all_businesses', vlasnik_show_all_businesses, methods=['GET'])
app.add_url_rule('/vlasnik_show_my_businesses', 'vlasnik_show_my_businesses', vlasnik_show_my_businesses, methods=['GET'])
app.add_url_rule('/vlasnik_show_routes', 'vlasnik_show_routes', vlasnik_show_routes, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
