from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..models.doctor import Doctor
from ..models.department import Department
from ..models.visit import Visit
from ..extensions import db

# 创建医生相关的蓝图
bp = Blueprint('doctor', __name__)


@bp.route('/doctor', methods=['POST'])
def create_doctor():
    # 解析请求数据
    data = request.get_json()

    # 验证请求数据格式
    if not data:
        return jsonify({
            "code": 400,
            "error": "INVALID_REQUEST",
            "message": "请求体必须是有效的JSON格式"
        }), 400

    # 提取并清洗数据
    name = data.get('Name', '').strip()
    dept_name = data.get('DeptName', '').strip()
    title = data.get('Title', '').strip()
    phone = data.get('Phone', '').strip()

    try:
        # 查询科室是否存在
        department = Department.query.filter_by(DeptName=dept_name).first()
        if not department:
            return jsonify({
                "code": 404,
                "error": "DEPT_NOT_EXIST",
                "message": "指定科室不存在"
            }), 404

        # 创建医生记录
        new_doctor = Doctor(
            Name=name,
            DeptID=department.DeptID,
            Title=title if title else None,  # 处理空值
            Phone=phone if phone else None
        )

        # 提交数据库事务
        db.session.add(new_doctor)
        db.session.commit()

        # 构造响应数据
        response_data = {
            "DoctorID": new_doctor.DoctorID,
            "Name": new_doctor.Name,
            "DeptID": department.DeptID,
            "DeptName": department.DeptName,
            "Title": new_doctor.Title,
            "Phone": new_doctor.Phone
        }

        return jsonify({
            "code": 201,
            "data": response_data
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "DATABASE_ERROR",
            "message": f"数据库操作失败: {str(e)}"
        }), 500

@bp.route('/doctor', methods=['GET'])
def get_doctors():
    try:
        # 获取查询参数
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('pageSize', default=10, type=int)
        dept_id = request.args.get('deptId', type=int)
        title = request.args.get('title', type=str)

        # 验证分页参数
        if page < 1 or page_size < 1:
            return jsonify({
                "code": 400,
                "error": "INVALID_PAGINATION",
                "message": "分页参数必须大于0"
            }), 400

        # 构建基础查询
        base_query = db.session.query(Doctor, Department.DeptName)\
            .join(Department, Doctor.DeptID == Department.DeptID)

        # 添加过滤条件
        if dept_id:
            base_query = base_query.filter(Doctor.DeptID == dept_id)
        if title:
            base_query = base_query.filter(Doctor.Title.ilike(f"%{title}%"))

        # 执行分页查询
        pagination = base_query.paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )

        # 构建返回数据
        doctors = []
        for doctor, dept_name in pagination.items:
            doctors.append({
                "DoctorID": doctor.DoctorID,
                "Name": doctor.Name,
                "DeptID": doctor.DeptID,
                "DeptName": dept_name,
                "Title": doctor.Title,
                "Phone": doctor.Phone
            })

        return jsonify({
            "code": 200,
            "data": {
                "total": pagination.total,
                "page": pagination.page,
                "pageSize": pagination.per_page,
                "list": doctors
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": f"服务器内部错误: {str(e)}"
        }), 500

@bp.route('/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_detail(doctor_id):
    try:
        # 联表查询医生信息和科室名称
        doctor_data = db.session.query(
            Doctor,
            Department.DeptName
        ).join(
            Department, Doctor.DeptID == Department.DeptID
        ).filter(
            Doctor.DoctorID == doctor_id
        ).first()

        if not doctor_data:
            return jsonify({
                "code": 404,
                "error": "DOCTOR_NOT_FOUND",
                "message": "医生不存在"
            }), 404

        doctor, dept_name = doctor_data

        # 构建响应数据
        response_data = {
            "DoctorID": doctor.DoctorID,
            "Name": doctor.Name,
            "DeptID": doctor.DeptID,
            "DeptName": dept_name,
            "Title": doctor.Title,
            "Phone": doctor.Phone
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

@bp.route('/doctor/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    try:
        # 查询医生是否存在
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({
                "code": 404,
                "error": "DOCTOR_NOT_FOUND",
                "message": "医生不存在"
            }), 404

        # 解析请求数据
        data = request.get_json()
        updates = {
            'Name': data.get('Name'),
            'DeptID': data.get('DeptID'),
            'Title': data.get('Title'),
            'Phone': data.get('Phone')
        }

        # 验证科室ID是否存在
        if 'DeptID' in data and data['DeptID']:
            dept = Department.query.get(data['DeptID'])
            if not dept:
                return jsonify({
                    "code": 404,
                    "error": "DEPT_NOT_EXIST",
                    "message": "科室不存在"
                }), 404

        # 应用更新字段
        for field, value in updates.items():
            if value is not None:
                # 字段长度验证
                if field == 'Name' and len(value) > 50:
                    return jsonify({
                        "code": 400,
                        "error": "NAME_TOO_LONG",
                        "message": "姓名不能超过50个字符"
                    }), 400
                setattr(doctor, field, value)

        db.session.commit()

        # 获取科室名称
        dept_name = Department.query.get(doctor.DeptID).DeptName

        return jsonify({
            "code": 200,
            "data": {
                "DoctorID": doctor.DoctorID,
                "Name": doctor.Name,
                "DeptID": doctor.DeptID,
                "DeptName": dept_name,
                "Title": doctor.Title,
                "Phone": doctor.Phone
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "DATABASE_ERROR",
            "message": f"数据库操作失败: {str(e)}"
        }), 500

@bp.route('/doctor/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    try:
        # 查询医生是否存在
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({
                "code": 404,
                "error": "DOCTOR_NOT_FOUND",
                "message": "医师不存在"
            }), 404

        # 检查是否存在关联就诊记录
        visit_count = Visit.query.filter_by(DoctorID=doctor_id).count()
        if visit_count > 0:
            return jsonify({
                "code": 400,
                "error": "HAS_VISIT_RECORDS",
                "message": "存在关联就诊记录，不可删除",
                "details": {
                    "relatedVisits": visit_count
                }
            }), 400

        # 执行删除
        db.session.delete(doctor)
        db.session.commit()

        return jsonify({
            "code": 204,
            "finish": True
        }), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "DATABASE_ERROR",
            "message": f"删除失败: {str(e)}"
        }), 500