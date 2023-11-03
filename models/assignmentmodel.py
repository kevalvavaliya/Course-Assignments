from db import db 


class AssignmentModel(db.Model):
    __tablename__="assignments"
    
    a_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    a_title = db.Column(db.String(200),unique=False,nullable=False)
    a_desc = db.Column(db.Text,nullable=False)
    
    # relation = db.relationship('RelationModel', back_populates='assignment', cascade='delete') 
    # users = db.relationship('User',secondary="student_assignment_association", back_populates='assignments', cascade='all, delete-orphan') 
    association = db.relationship('AssociationModel', back_populates='assignment', cascade='all, delete-orphan') 


