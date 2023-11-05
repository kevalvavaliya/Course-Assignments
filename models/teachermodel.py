from db import db

class TeacherModel(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(100),nullable=False)

    assignments = db.relationship('AssignmentModel',back_populates='teacher',cascade='all, delete-orphan')
    usertype="teacher"

    def __init__(self, email, password,name):
      self.email = email
      self.password = password
      self.name = name

    
    def __str__(self):
        return f"{self.email} , {self.name} , {self.usertype} , {self.id}"
    