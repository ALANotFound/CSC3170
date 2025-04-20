from ..extensions import db

class Patient(db.Model):
    __tablename__ = 'Patient'
    
    PatientID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Gender = db.Column(db.String(50))
    BirthDate = db.Column(db.Date)
    IdentityNo = db.Column(db.String(255), nullable=False, unique=True)
    Phone = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Patient {self.Name}>'