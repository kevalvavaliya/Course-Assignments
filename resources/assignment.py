from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AssignmentSchema,AssignmentUpdateSchema
from db import db
from models.assignmentmodel import AssignmentModel
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp = Blueprint("Assignment",__name__,description="Assignment service")

# ASSIGNMENT CLASS for fetching,deleting and updating assignment using ID
@blp.route("/assignment/<int:assignment_id>")
class Assignment(MethodView):

    # GET method for FETCHING specific assignment using Assignment ID
    @blp.response(200,AssignmentSchema)
    def get(self,assignment_id):
        assignment = AssignmentModel.query.get_or_404(assignment_id,description=f"No assignment found")
        return assignment
    
    # DELETE method for DELETING specific assignment using Assignment ID 
    def delete(self,assignment_id):
        assignment = AssignmentModel.query.get_or_404(assignment_id)
        try:
            db.session.delete(assignment)
            db.session.commit()
        except:
            abort(500,message="An error occured while deleting assignment.")
        return {"message":"Assignment deleted"}, 200
    
    # PUT method for UPDATING specific assignment using Assignment ID 
    @blp.arguments(AssignmentUpdateSchema)
    @blp.response(200,AssignmentUpdateSchema)
    def put(self,assignment_data,assignment_id):
        update_title = assignment_data.get("title")
        update_desc = assignment_data.get("desc")
        
        assignment = AssignmentModel.query.get_or_404(assignment_id,description=f"No assignment found")
        
        if update_title is not None:
            assignment.title = update_title
        if update_desc is not None:
            assignment.desc = update_desc
        try:
            db.session.add(assignment)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e.__cause__)
            abort(500,message="An error occured while updating assignment.")

        return assignment
    

# ASSIGNMENT LIST CLASS for fetching list of assignments and adding a new assignment
@blp.route("/assignment")
class AssignmentList(MethodView):
    
    # GET method to get all assignments 
    @blp.response(200,AssignmentSchema(many=True))
    def get(self):
        return AssignmentModel.query.all()

    # POST method to add new assignment
    @blp.arguments(AssignmentSchema)
    @blp.response(201,AssignmentSchema)
    def post(self,assignment_data):
        title = assignment_data.get("title")
        desc = assignment_data.get("desc")

        assignment = AssignmentModel(title=title,desc=desc)
        try:
            db.session.add(assignment)
            db.session.commit()
        except IntegrityError:
            abort(400,message="An Assignment with that title already exists.")
        except SQLAlchemyError as e:
            abort(500,message="An error occured while creating assignment.")
        
        return assignment

