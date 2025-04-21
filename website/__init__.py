from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


def create_database(app):
    with app.app_context():
        db.create_all()
        print('✅ Database Created')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    # 404 Error page
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Customer, Cart, Product, Order

    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))

    # Blueprints
    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    return app
