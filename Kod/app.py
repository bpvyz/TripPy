from init import create_app
from routes import login, dashboard, logout

app = create_app()

# Routes
app.add_url_rule('/', 'login', login)
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/dashboard', 'dashboard', dashboard)
app.add_url_rule('/logout', 'logout', logout)

if __name__ == '__main__':
    app.run(debug=True)
