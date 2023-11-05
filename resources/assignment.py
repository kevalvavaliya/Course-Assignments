from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AssignmentSchema,AssignmentUpdateSchema
from db import db
from models.assignmentmodel import AssignmentModel
from flask_jwt_extended import jwt_required, get_jwt,current_user
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
    @jwt_required() 
    def delete(self,assignment_id):
        
    
        if(current_user.usertype!="teacher"):
            abort(401, message="Teacher privilege required.")

        assignment = AssignmentModel.query.get_or_404(assignment_id)
        
        ## Checking current user id from JWT with teacher id who created assignment
        if(assignment.teacher_id!=current_user.id):
            abort(401,message="Only teacher which created assignment can delete it")
        try:
            db.session.delete(assignment)
            db.session.commit()
        except:
            abort(500,message="An error occured while deleting assignment.")
        return {"message":"Assignment deleted"}, 200
    
    # PUT method for UPDATING specific assignment using Assignment ID 
    @jwt_required()
    @blp.arguments(AssignmentUpdateSchema)
    @blp.response(200,AssignmentUpdateSchema)
    def put(self,assignment_data,assignment_id):

        if(current_user.usertype!="teacher"):
            abort(401, message="Teacher privilege required.")

        update_title = assignment_data.get("title")
        update_desc = assignment_data.get("desc")
        update_teacher = assignment_data.get("teacher_id")

        assignment = AssignmentModel.query.get_or_404(assignment_id,description=f"No assignment found")

        ## Checking current user id from JWT with teacher id who created assignment
        if(assignment.teacher_id!=current_user.id):
            abort(401,message="Only teacher which created assignment can delete it")
        
        if update_title is not None:
            assignment.title = update_title
        if update_desc is not None:
            assignment.desc = update_desc
        if update_teacher is not None:
            assignment.teacher_id = update_teacher
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
    @jwt_required()
    @blp.arguments(AssignmentSchema)
    @blp.response(201,AssignmentSchema)
    def post(self,assignment_data):

        # Allowing only teacher to create assignment using jwt claims
        # jwt = get_jwt()
        # if not jwt.get("is_teacher"):
        #     abort(401, message="Teacher privilege required.")
        
        ## Checking current user id from JWT with teacher id who created assignment
        if(current_user.usertype!="teacher"):
            abort(401, message="Teacher privilege required.")

        title = assignment_data.get("title")
        desc = assignment_data.get("desc")
        teacher_id = current_user.id

        assignment = AssignmentModel(title=title,desc=desc,teacher_id=teacher_id)
        try:
            db.session.add(assignment)
            db.session.commit()
        except IntegrityError:
            abort(409,message="An Assignment with that title already exists or Teacher with that id do not exists")
        except SQLAlchemyError as e:
            abort(500,message="An error occured while creating assignment.")
        
        return assignment

