import os

# external
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


# internal
from config import app_config

# Variable initialization
db = SQLAlchemy()
login_manager = LoginManager()
# database object which we will use to interact with the database.


# create_app function given a configuration name, loads the correct
# configuration from the config.py file, as well as the configurations
# from the instance/config.py file.
migrate = Migrate()

def create_app():
    # Initialize the app
    app = Flask(__name__, instance_relative_config=True)

    # Use FLASK_CONFIG environment variable, default to 'development' if not set
    config_name = os.getenv('FLASK_CONFIG', 'development')

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_message = "You are not authorised to see this page. Please log in!"
    login_manager.login_view = "auth.login"

    from myapp import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page not found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app