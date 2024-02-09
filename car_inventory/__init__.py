from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


#internal imports
from config import Config
from .models import login_manager, db
from .blueprints.site.routes import site
from .blueprints.auth.routes import auth
from .blueprints.api.routes import api
from .helpers import JSONEncoder



#instantiating our Flask app
app = Flask(__name__)

#going to tell our app what Class to look to for configuration
app.config.from_object(Config)
jwt = JWTManager(app) #allows our app to use JWTManager from anywhere (added security for our api routes)


#wrap our app in login_manager so we can use it wherever in our app
login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in' 
login_manager.login_message = "Hey you! Log in please!"
login_manager.login_message_category = 'warning'


#creating our first route using the @route decorator
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)


#instantiating our datbase & wrapping our app
db.init_app(app)
migrate = Migrate(app, db) #things we are connecting/migrating (our application to our database)
app.json_encoder = JSONEncoder  #we are not instantiating an object we are simply pointing to this class we made when we need to encode data objects
cors = CORS(app) #Cross Origin Resource Sharing aka allowing other apps to talk to our flask app/server



