from flask import Flask
from config import Config
from .blueprints.site.routes import site


app = Flask(__name__)


app.config.from_object(Config)


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

app.register_blueprint(site)