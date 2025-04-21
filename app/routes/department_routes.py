from flask import Blueprint, request, jsonify
from ..models.department import Department
from ..models.doctor import Doctor
from ..models.ward import Ward
from ..extensions import db
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
        # 生成不重复的科室ID逻辑
        max_id = db.session.query(func.max(Department.DeptID)).scalar() or 0
        new_id = max_id + 1

        # 检查新ID是否已被占用（防止并发冲突）
        while Department.query.get(new_id):
            new_id += 1

        # 创建带自定义ID的科室
        new_dept = Department(DeptID=new_id, DeptName=dept_name, Location=location)
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


@bp.route('/department/<int:dept_id>', methods=['GET'])
def get_department(dept_id):
    try:
        # 查询科室基本信息
        department = Department.query.get(dept_id)

        if not department:
            return jsonify({
                "code": 404,
                "error": "DEPT_NOT_FOUND",
                "message": "科室不存在"
            }), 404

        # 获取关联病房信息
        wards = Ward.query.filter_by(DeptID=dept_id).all()
        ward_list = [{
            "WardID": w.WardID,
            "WardName": w.WardName,
            "Floor": w.Floor,
            "Capacity": w.Capacity
        } for w in wards]

        # 获取关联医生信息
        doctors = Doctor.query.filter_by(DeptID=dept_id).all()
        doctor_list = [{
            "DoctorID": d.DoctorID,
            "Name": d.Name,
            "Title": d.Title,
            "Phone": d.Phone
        } for d in doctors]

        # 构建响应数据
        response_data = {
            "DeptID": department.DeptID,
            "DeptName": department.DeptName,
            "Location": department.Location,
            "Wards": ward_list,
            "Doctors": doctor_list
        }

        return jsonify({
            "code": 200,
            "data": response_data
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": f"服务器内部错误: {str(e)}"
        }), 500


@bp.route('/department/<int:dept_id>', methods=['PUT'])
def update_department(dept_id):
    try:
        # 获取科室实例
        department = Department.query.get(dept_id)
        if not department:
            return jsonify({
                "code": 404,
                "error": "DEPT_NOT_EXIST",
                "message": "科室ID不存在"
            }), 404

        # 解析请求数据
        data = request.get_json()
        new_name = data.get('DeptName', '').strip()
        new_location = data.get('Location', '').strip()

        # 验证必填字段
        if not new_name:
            return jsonify({
                "code": 400,
                "error": "INVALID_DEPTNAME",
                "message": "科室名称不能为空"
            }), 400

        # 执行更新
        department.DeptName = new_name
        if new_location:  # 允许清空位置信息
            department.Location = new_location

        db.session.commit()

        # 返回更新后的数据
        return jsonify({
            "code": 200,
            "data": {
                "DeptID": department.DeptID,
                "DeptName": department.DeptName,
                "Location": department.Location
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "DATABASE_ERROR",
            "message": f"数据库更新失败: {str(e)}"
        }), 500