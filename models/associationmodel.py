from db import db


class AssociationModel(db.Model):
    __tablename__ = "student_assignment_association"

    association_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column( db.Integer, db.ForeignKey('users.uid',ondelete="CASCADE"))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.aid',ondelete="CASCADE"))

    user = db.relationship('UserModel', back_populates='association') 
    assignment = db.relationship('AssignmentModel', back_populates='association') 

