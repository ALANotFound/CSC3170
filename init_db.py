from app import create_app
from app.extensions import db
from app.models.department import Department
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.ward import Ward
from app.models.admission import Admission
from app.models.visit import Visit

app = create_app()

with app.app_context():
    # 创建所有表
    db.create_all()
    print("数据库表已创建") 