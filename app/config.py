import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/hospital_data' # 更改成你自己的 username:password@localhost:host/databasename
    SQLALCHEMY_TRACK_MODIFICATIONS = False