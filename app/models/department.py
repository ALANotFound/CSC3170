from ..extensions import db

class Department(db.Model):
    __tablename__ = 'Department'
    
    DeptID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DeptName = db.Column(db.String(255), nullable=False, unique=True)
    Location = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Department {self.DeptName}>'