from marshmallow import Schema,fields

class UserLoginSchema(Schema):
    email = fields.Str(required=True,error_messages={"required": "email is required."})
    password = fields.Str(required=True,error_messages={"required": "Password is required."},load_only=True)
    name = fields.Str()
    usertype = fields.Str(missing="student")

class UserRegisterSchema(Schema):
    email = fields.Str(required=True,error_messages={"required": "email is required."})
    password = fields.Str(required=True,error_messages={"required": "Password is required."},load_only=True)
    name = fields.Str(required=True,error_messages={"required": "name is required."})
    usertype = fields.Str(missing="student")    

class AssignmentSchema(Schema):
    aid = fields.Int(dump_only=True,required=True)
    title = fields.Str(required=True,error_messages={"required": "Assignment title is required."})
    desc  = fields.Str(required=True,error_messages={"required":"Assignment description is required."})
    teacher_id = fields.Int(dump_only=True)

class AssignmentUpdateSchema(Schema):
    aid = fields.Int(dump_only=True)
    title = fields.Str( )
    desc  = fields.Str()
    teacher_id = fields.Int()
    
class AssignmentPaginationSchema(Schema):
    pagesize = fields.Int()
    pageRows = fields.Int()

    
    