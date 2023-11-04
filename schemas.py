from marshmallow import Schema,fields

class UserLoginSchema(Schema):
    username = fields.Str(required=True,error_messages={"required": "Username is required."})
    password = fields.Str(required=True,error_messages={"required": "Password is required."})

class AssignmentSchema(Schema):
    aid = fields.Int(dump_only=True,required=True)
    title = fields.Str(required=True,error_messages={"required": "Assignment title is required."})
    desc  = fields.Str(required=True,error_messages={"required":"Assignment description is required."})

class AssignmentUpdateSchema(Schema):
    aid = fields.Int(dump_only=True)
    title = fields.Str( )
    desc  = fields.Str()
    