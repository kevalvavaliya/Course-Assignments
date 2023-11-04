from db import db 

class UserModel(db.Model):

    __tablename__ = "users"
    uid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)

    # relation = db.relationship('RelationModel', back_populates='user', cascade='delete') 
    association = db.relationship('AssociationModel', back_populates='user', cascade='all, delete-orphan') 

    def __init__(self, username, password):
      self.username = username
      self.password = password

    def __str__(self):
        return self.username
    
    
    
