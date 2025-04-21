from ..extensions import db

class Doctor(db.Model):
    __tablename__ = 'Doctor'
    
    DoctorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    DeptID = db.Column(db.Integer, db.ForeignKey('Department.DeptID'), nullable=False)
    Title = db.Column(db.String(255))
    Phone = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Doctor {self.Name}>'