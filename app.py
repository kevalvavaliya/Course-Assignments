from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from resources.auth import blp as Auth
from resources.assignment import blp as Assignment
from db import db
import models

# intializing Flask app
app = Flask(__name__)
CORS(app)


# Configuration for api reference and doc using swagger
app.config["PROPAGATE_EXCEPTIONS"]=True
app.config["API_TITLE"]="Keval Playpower Labs Backend Task"
app.config["API_VERSION"]="v1"
app.config["OPENAPI_VERSION"]="3.0.3"
app.config["OPENAPI_URL_PREFIX"]="/"
app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/"

# configuration for database 
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:@localhost:3306/playpower"
db.init_app(app)

api = Api(app)

with app.app_context():
    db.create_all()

# Registering Service Blueprints
api.register_blueprint(Auth)
api.register_blueprint(Assignment)
