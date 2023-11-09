from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from resources.auth import blp as Auth
from resources.assignment import blp as Assignment
from db import db
import models
import datetime
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# intializing Flask app
def create_app():
    app = Flask(__name__)
    CORS(app)
    load_dotenv()

    # Configuration for api reference and doc using swagger
    app.config["PROPAGATE_EXCEPTIONS"]=True
    app.config["API_TITLE"]="Keval Playpower Labs Backend Task"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]="3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/"

    # configuration for database 
    app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
    db.init_app(app)

    api = Api(app)

    # jwt configuration
    app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=5)

    jwt = JWTManager(app)

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity.get("usertype") == "teacher":
    #         return {"is_teacher": True}
    #     return {"is_teacher": False}

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers,jwt_data):
        
        email=jwt_data['sub']['email']
        
        user = models.UserModel.query.filter_by(email=email).first()
        if not user:
            user = models.TeacherModel.query.filter_by(email=email).first()

        return user

    # creating tables from models in db
    with app.app_context():
        db.create_all()

    # Registering Service Blueprints
    api.register_blueprint(Auth)
    api.register_blueprint(Assignment)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0',port=5000, debug=True)