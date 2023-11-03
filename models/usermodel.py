from db import db 

student_assignment_association = db.Table(
    'student_assignment',
    db.Column('user_id', db.Integer, db.ForeignKey('users.u_id',ondelete="CASCADE"),),
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignments.a_id',ondelete="CASCADE"))
)

class UserModel(db.Model):

    __tablename__ = "users"
    u_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),unique=True,nullable=False)

    # relation = db.relationship('RelationModel', back_populates='user', cascade='delete') 
    assignments = db.relationship('User',secondary="student_assignment_association", back_populates='users', cascade='all, delete-orphan') 


    
    
