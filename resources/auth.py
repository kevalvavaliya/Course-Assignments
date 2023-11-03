from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("Auth",__name__,description="Authentication service")

@blp.route("/")
class Auth(MethodView):
    
    def get(self):
        return "Auth service running"
    
    def post(self):
        pass