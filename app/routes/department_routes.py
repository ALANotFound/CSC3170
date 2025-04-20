from flask import Blueprint, request, jsonify
from app.models.department import Department
from app.models.doctor import Doctor
from app.extensions import db
from sqlalchemy import func

bp = Blueprint('department', __name__)

@bp.route('/department', methods=['POST'])
def create_department(): # 创建科室
    # 解析 json body
    data = request.get_json()
    
    dept_name = data['DeptName'].strip()
    location = data.get('Location', '').strip()
    
    # 检查科室是否已存在
    existing_dept = Department.query.filter_by(DeptName=dept_name).first()
    if existing_dept:
        return jsonify({
            "code": 400,
            "error": "DUPLICATE_DEPARTMENT",
            "message": "科室已存在"
        }), 400

    try:
        # 创建新科室
        new_dept = Department(DeptName=dept_name, Location=location)
        db.session.add(new_dept)
        db.session.commit()

        # 返回创建结果
        return jsonify({
            "code": 201,
            "data": {
                "DeptID": new_dept.DeptID,
                "DeptName": new_dept.DeptName,
                "Location": new_dept.Location
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "DATABASE_ERROR",
            "message": str(e)
        }), 500
    
@bp.route('/department', methods=['GET'])
def get_departments():
    # 获取分页参数
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)

    # 验证参数有效性
    if page < 1 or page_size < 1:
        return jsonify({
            "code": 400,
            "error": "INVALID_PAGINATION",
            "message": "分页参数必须大于 0"
        }), 400

    try:
        # 获取分页数据并统计医生数量
        pagination = db.session.query(
            Department,
            func.count(Doctor.DoctorID).label('doctor_count')
        ).outerjoin(
            Doctor, Department.DeptID == Doctor.DeptID
        ).group_by(Department.DeptID).paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )

        # 构建返回数据结构
        departments = []
        for dept, doctor_count in pagination.items:
            departments.append({
                "DeptID": dept.DeptID,
                "DeptName": dept.DeptName,
                "Location": dept.Location,
                "DoctorNo": doctor_count
            })

        return jsonify({
            "code": 200,
            "data": {
                "total": pagination.total,
                "page": pagination.page,
                "pageSize": pagination.per_page,
                "list": departments
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": "服务器内部错误"
        }), 500