from flask import Flask
from .config import configs
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager

def register_blueprints(app):
	from .handlers import front, admin, course, live
	app.register_blueprint(front)
	app.register_blueprint(admin)
	app.register_blueprint(course)
	app.register_blueprint(live)

def register_extends(app):
	db.init_app(app)
	Migrate(app, db)

	login_manager = LoginManager()
	login_manager.init_app(app)
	@login_manager.user_loader
	def load_user(id):
		return User.query.get(id)

	login_manager.login_view = 'front.login'



def create_app(config):
	app = Flask(__name__)
	app.config.from_object(configs.get(config))
	register_blueprints(app)
	register_extends(app)
	return app
