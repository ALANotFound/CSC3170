from ..extensions import db

class Admission(db.Model):
    __tablename__ = 'Admission'
    
    AdmissionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    WardID = db.Column(db.Integer, db.ForeignKey('Ward.WardID'), nullable=False)
    BedNo = db.Column(db.String(50))
    AdmissionDate = db.Column(db.Date, nullable=False)
    DischargeDate = db.Column(db.Date)
    AdmissionReason = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Admission {self.AdmissionID}>'