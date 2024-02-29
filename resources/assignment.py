from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AssignmentSchema,AssignmentUpdateSchema,AssignmentPaginationSchema
from db import db
from models.assignmentmodel import AssignmentModel
from models.usermodel import UserModel
from models.associationmodel import AssociationModel
from flask_jwt_extended import jwt_required, get_jwt,current_user
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from util.sendemail import Email


blp = Blueprint("Assignment",__name__,description="Assignment service")

## documenting headers
Autheaders={
            "Authorization": {
                "description": "User's authentication token (Bearer token)",
                "required": True,
                "type": "string"
            }
    }


# ASSIGNMENT CLASS for fetching,deleting and updating assignment using ID
@blp.route("/assignment/<int:assignment_id>")
class Assignment(MethodView):

    # GET method for FETCHING specific assignment using Assignment ID
    @blp.response(200,AssignmentSchema)
    @blp.doc(summary="Get assignment using assignment id",)   
    def get(self,assignment_id):
        assignment = AssignmentModel.query.get_or_404(assignment_id,description=f"No assignment found")
        return assignment
    
    # DELETE method for DELETING specific assignment using Assignment ID
    @jwt_required() 
    @blp.doc(summary="Delete assignment using assignment id",)  
    @blp.response(200,description="Assignment deleted",headers=Autheaders) 
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
    @blp.response(200,AssignmentUpdateSchema,description="Assignment updated",headers=Autheaders)
    @blp.doc(summary="Update assignment using assignment id",)   
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
    @blp.doc(summary="Get All assignment",)   
    def get(self):
        return AssignmentModel.query.all()

    # POST method to add new assignment
    @jwt_required()
    @blp.arguments(AssignmentSchema)
    @blp.response(201,schema=AssignmentSchema,description="Sucess",headers=Autheaders)
    @blp.doc(description="Create Assignment",
         summary="Create assignment",)   
    def post(self,assignment_data):
        
        ## Checking current user id from JWT with teacher id who created assignment
        if(current_user.usertype!="teacher"):
            abort(401, message="Teacher privilege required.")
            

        title = assignment_data.get("title")
        desc = assignment_data.get("desc")
        teacher_id = current_user.id

        assignment = AssignmentModel(title=title,desc=desc,teacher_id=teacher_id)
        try:
            db.session.add(assignment)

            ## Assigning assignment to all students and sending
            studentList = UserModel.getAllStudents()

            associationList = AssociationModel.getListToAssign(students_list=studentList,assignment=assignment)
            
            emailResponse = Email.sendEmailToAllStudents(studentList,assignment,current_user.name)
            if(emailResponse.status_code==200):
                db.session.add_all(associationList)
                db.session.commit()
            else:
                print(emailResponse.text)
                abort(500,message="An error occured while sending assignment emails.")

        except IntegrityError:
            abort(409,message="An Assignment with that title already exists or Teacher with that id do not exists")
        except SQLAlchemyError as e:
            abort(500,message="An error occured while creating assignment.")
        
        return assignment


# @blp.route("/assignmentListPagination")
# class AssignmentListTest(MethodView):
#     @blp.response(201,schema=AssignmentSchema,description="Sucess",many=True)
#     @blp.arguments(AssignmentPaginationSchema)
#     def post(self,data):
#         pageSize = data.get('pagesize')
#         pageRows = data.get('pageRows')
#         ans = AssignmentModel.query.limit(pageRows).all()
#         print(ans)

#         # return  "temporary respone"
#         return AssignmentModel.query.limit(pageRows,).all()
