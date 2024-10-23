from flask import Flask, request
from flask_babel import Babel, _

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'sr']

    babel = Babel(app)
    def get_locale():
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
    @app.context_processor
    def inject_get_locale():
        return dict(get_locale=get_locale)

    babel.init_app(app,locale_selector=get_locale)

    from mappings.tables import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

app = create_app()
