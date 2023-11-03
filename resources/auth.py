from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserLoginSchema
# from passlib.hash import pbkdf2_sha256
from db import db
from models import UserModel
from flask_jwt_extended import create_access_token


blp = Blueprint("Auth",__name__,description="Authentication service")

@blp.route("/login")
class UserLogin(MethodView):
    
    # def get(self):
    #     return "Auth service running"

    @blp.arguments(UserLoginSchema)
    # @blp.response(200,UserLoginSchema)
    def post(self,userdata):
        username = userdata["username"]
        password = userdata["password"]

        user = UserModel.query.filter_by(username=username).one_or_404(
            description=f"No user named '{username}' exists."
        )   
        if user:
            access_token = create_access_token(identity=user.username)
            return {"message":"user login success","acess_token":access_token}, 200     
        abort(401, message="Invalid credentials.")


        

@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserLoginSchema)
    def post(self,user_data):
        username = user_data.get("username")
        password = user_data.get("password")
        if UserModel.query.filter(UserModel.username==username).first():
            abort(409,message="A user with that username already exists.")
        
        user = UserModel(username=username,password=password)

        db.session.add(user)
        db.session.commit()
        
        return {"message": "User created successfully."}, 201

