from ..extensions import db

class Visit(db.Model):
    __tablename__ = 'Visit'
    
    VisitID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('Patient.PatientID'), nullable=False)
    DoctorID = db.Column(db.Integer, db.ForeignKey('Doctor.DoctorID'), nullable=False)
    AdmissionID = db.Column(db.Integer, db.ForeignKey('Admission.AdmissionID'), nullable=True)
    VisitDate = db.Column(db.Date)
    Complaint = db.Column(db.Text)
    Diagnosis = db.Column(db.Text)
    Prescription = db.Column(db.Text)
    Fee = db.Column(db.DECIMAL(10, 2))
    
    def __repr__(self):
        return f'<Visit {self.VisitID}>'