from ..extensions import db

class Ward(db.Model):
    __tablename__ = 'Ward'
    
    WardID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    WardName = db.Column(db.String(255), nullable=False)
    Floor = db.Column(db.Integer)
    Capacity = db.Column(db.Integer)
    DeptID = db.Column(db.Integer, db.ForeignKey('Department.DeptID'), nullable=False)
    
    def __repr__(self):
        return f'<Ward {self.WardName}>'