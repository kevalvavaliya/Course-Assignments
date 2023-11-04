from db import db 


class AssignmentModel(db.Model):
    __tablename__="assignments"
    
    aid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),unique=True,nullable=False)
    desc = db.Column(db.Text,nullable=False)
    
    # relation = db.relationship('RelationModel', back_populates='assignment', cascade='delete') 
    # users = db.relationship('User',secondary="student_assignment_association", back_populates='assignments', cascade='all, delete-orphan') 
    association = db.relationship('AssociationModel', back_populates='assignment', cascade='all, delete-orphan') 

    def __str__(self):
        return f"Assignment Title : {self.title} \nAssignment Description : {self.desc}"
    
