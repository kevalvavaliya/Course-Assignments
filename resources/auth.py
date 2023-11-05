from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserLoginSchema,UserRegisterSchema
# from passlib.hash import pbkdf2_sha256
from db import db
from models import UserModel,TeacherModel
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError,IntegrityError


blp = Blueprint("Auth",__name__,description="Authentication service")


@blp.route("/login")
class UserLogin(MethodView):

    # POST METHOD FOR LOGIN
    @blp.arguments(UserLoginSchema)
    def post(self,user_data):
        email = user_data.get("email")
        password = user_data.get("password")
        usertype = user_data.get("usertype")

        if(usertype=="student"):
            user = UserModel.query.filter_by(email=email,password=password).first()
            
        elif(usertype=="teacher"):
            user = TeacherModel.query.filter_by(email=email,password=password).first()
        else:
            abort(401,message="Invalid user type")
        
        if user is not None:
            access_token = create_access_token(identity={"email":user.email,"id":user.id})  # creating JWT token 
            return {"message":"user login success","acess_token":access_token}, 200     
        abort(401, message="Invalid credentials.")


        

@blp.route("/register")
class UserRegister(MethodView):

    # POST METHOD FOR REGISTERING USER
    @blp.arguments(UserRegisterSchema)
    def post(self,user_data):
        email = user_data.get("email")
        password = user_data.get("password")
        usertype = user_data.get("usertype")
        name = user_data.get("name")

        if(usertype=="student"):
            user = UserModel(email=email,password=password,name=name)
        elif(usertype=="teacher"):
            user = TeacherModel(email=email,password=password,name=name)  
        else:
            abort(401,message="Invalid User type")  
        try:
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully."}, 201
        except IntegrityError as e:
            abort(409,message="A user with that email already exists.")
        except SQLAlchemyError as e:
             abort(500, message="An error occurred while registering the user.")

