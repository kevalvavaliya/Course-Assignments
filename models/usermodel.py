from db import db 

class UserModel(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),unique=True,nullable=False)
    name = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200),nullable=False)

    # relation = db.relationship('RelationModel', back_populates='user', cascade='delete') 
    association = db.relationship('AssociationModel', back_populates='user', cascade='all, delete-orphan') 
    usertype="student"
    
    def __init__(self, email, password,name):
      self.email = email
      self.password = password
      self.name = name
      
    
    def __str__(self):
        return f"{self.email} , {self.name} , {self.usertype} , {self.id}"
    
    @classmethod
    def getAllStudents(cls):
       return cls.query.all()
    
    
    
