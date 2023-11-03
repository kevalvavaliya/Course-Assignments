from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("Assignment",__name__,description="Assignment service")

@blp.route("/")
class Assignment(MethodView):
    
    def get(self):
        return "Assignment service running"
    
    def post(self):
        pass