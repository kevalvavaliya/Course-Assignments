from marshmallow import Schema,fields

class UserLoginSchema(Schema):
    username = fields.Str(required=True,error_messages={"required": "Username is required."})
    password = fields.Str(required=True,error_messages={"required": "Password is required."})


