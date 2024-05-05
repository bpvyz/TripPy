from init import create_app
from routes import login, logout, register, verify, putnik_dashboard, vlasnik_dashboard, admin_dashboard, logout, add_route, show_all_routes

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
app.add_url_rule('/add_route', 'add_route', add_route, methods=['GET', 'POST'])
app.add_url_rule('/show_all_routes', 'show_all_routes', show_all_routes, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
