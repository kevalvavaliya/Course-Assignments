from db import db


class AssociationModel(db.Model):
    __tablename__ = "student_assignment_association"

    association_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column( db.Integer, db.ForeignKey('users.id',ondelete="CASCADE"))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.aid',ondelete="CASCADE"))

    user = db.relationship('UserModel', back_populates='association') 
    assignment = db.relationship('AssignmentModel', back_populates='association') 

    @classmethod
    def getListToAssign(cls,students_list,assignment):
        aList=[]
        for student in students_list:
            aList.append(AssociationModel(user_id=student.id,assignment_id=assignment.aid))
        return aList