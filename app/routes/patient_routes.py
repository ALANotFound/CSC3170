from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..models.doctor import Doctor
from ..models.department import Department
from ..models.admission import Admission
from ..models.visit import Visit
from ..extensions import db

bp = Blueprint('patient', __name__)

from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from ..models.patient import Patient  # 确保有此模型
from ..extensions import db

bp = Blueprint('patient', __name__)


@bp.route('/patient', methods=['POST'])
def create_patient():
    # 参数校验框架
    required_fields = ['Name', 'Gender', 'IdentityNo']
    data = request.get_json()

    # 检查必填字段
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({
            "code": 400,
            "error": "MISSING_REQUIRED_FIELDS",
            "message": f"缺少必填字段: {', '.join(missing)}"
        }), 400

    # 字段长度校验
    if len(data['Name']) > 50:
        return jsonify({
            "code": 400,
            "error": "NAME_TOO_LONG",
            "message": "姓名不能超过50个字符"
        }), 400

    # 身份证格式校验（简单版）
    if not data['IdentityNo'].isdigit() or len(data['IdentityNo']) != 18:
        return jsonify({
            "code": 400,
            "error": "INVALID_IDENTITY_NO",
            "message": "身份证号必须为18位数字"
        }), 400

    # 日期格式校验
    if 'BirthDate' in data:
        try:
            datetime.strptime(data['BirthDate'], '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "code": 400,
                "error": "INVALID_DATE_FORMAT",
                "message": "日期格式应为YYYY-MM-DD"
            }), 400

    # 手机号格式校验
    if 'Phone' in data and data['Phone']:
        phone = data['Phone'].strip()
        if not (phone.startswith('1') and len(phone) == 11 and phone.isdigit()):
            return jsonify({
                "code": 400,
                "error": "INVALID_PHONE",
                "message": "手机号格式不正确"
            }), 400
        data['Phone'] = phone  # 标准化存储

    try:
        # 创建患者记录
        new_patient = Patient(
            Name=data['Name'].strip(),
            Gender=data['Gender'].strip(),
            BirthDate=data.get('BirthDate'),
            IdentityNo=data['IdentityNo'].strip(),
            Phone=data.get('Phone', '').strip()
        )
        db.session.add(new_patient)
        db.session.commit()

        # 构建响应数据
        patient_data = {
            "PatientID": new_patient.PatientID,
            "Name": new_patient.Name,
            "Gender": new_patient.Gender,
            "BirthDate": new_patient.BirthDate.isoformat() if new_patient.BirthDate else None,
            "IdentityNo": new_patient.IdentityNo,
            "Phone": new_patient.Phone
        }

        return jsonify({
            "code": 201,
            "data": patient_data
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        if 'IdentityNo' in str(e.orig):
            return jsonify({
                "code": 409,
                "error": "DUPLICATE_IDENTITY_NO",
                "message": "身份证号已存在"
            }), 409
        return jsonify({
            "code": 500,
            "error": "DATABASE_ERROR",
            "message": "数据库操作失败"
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": "服务器内部错误"
        }), 500

@bp.route('/patient', methods=['GET'])
def get_patients():
    try:
        # 解析查询参数
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('pageSize', default=20, type=int)
        name = request.args.get('surname', type=str)

        # 参数验证
        if page < 1 or page_size < 1:
            return jsonify({
                "code": 400,
                "error": "INVALID_PAGINATION",
                "message": "分页参数必须大于0"
            }), 400

        # 构建基础查询
        base_query = Patient.query.order_by(Patient.PatientID.desc())

        # 添加姓名过滤
        if name and name.strip():
            search_name = f"%{name.strip()}%"
            base_query = base_query.filter(Patient.Name.ilike(search_name))

        # 执行分页查询
        pagination = base_query.paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )

        # 构建响应数据
        patients = []
        for patient in pagination.items:
            patients.append({
                "PatientID": patient.PatientID,
                "Name": patient.Name,
                "Gender": patient.Gender,
                "BirthDate": patient.BirthDate.isoformat() if patient.BirthDate else None,
                "Phone": patient.Phone
            })

        return jsonify({
            "code": 200,
            "data": {
                "total": pagination.total,
                "page": pagination.page,
                "pageSize": pagination.per_page,
                "list": patients
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": f"服务器内部错误: {str(e)}"
        }), 500


@bp.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient_detail(patient_id):
    try:
        # 查询患者信息
        patient = Patient.query.get(patient_id)

        if not patient:
            return jsonify({
                "code": 404,
                "error": "PATIENT_NOT_FOUND",
                "message": "患者不存在"
            }), 404

        # 构建响应数据
        patient_data = {
            "PatientID": patient.PatientID,
            "Name": patient.Name,
            "Gender": patient.Gender,
            "BirthDate": patient.BirthDate.strftime("%Y-%m-%d") if patient.BirthDate else None,
            "IdentityNo": patient.IdentityNo,
            "Phone": patient.Phone
        }

        return jsonify({
            "code": 200,
            "data": patient_data
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": f"服务器内部错误: {str(e)}"
        }), 500


@bp.route('/patient/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    try:
        # 查询患者是否存在
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({
                "code": 404,
                "error": "PATIENT_NOT_FOUND",
                "message": "患者不存在"
            }), 404

        data = request.get_json()

        # 字段更新逻辑
        if 'Name' in data:
            new_name = data['Name'].strip()
            if len(new_name) > 50:
                return jsonify({
                    "code": 400,
                    "error": "INVALID_NAME",
                    "message": "姓名不能超过50个字符"
                }), 400
            patient.Name = new_name

        if 'Gender' in data:
            gender = data['Gender'].strip()
            if gender not in ['男', '女']:
                return jsonify({
                    "code": 400,
                    "error": "INVALID_GENDER",
                    "message": "性别必须为'男'或'女'"
                }), 400
            patient.Gender = gender

        if 'BirthDate' in data:
            try:
                birth_date = datetime.strptime(data['BirthDate'], '%Y-%m-%d').date()
                patient.BirthDate = birth_date
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "INVALID_DATE",
                    "message": "日期格式应为YYYY-MM-DD"
                }), 400

        if 'Phone' in data:
            phone = data['Phone'].strip()
            if phone and not (phone.startswith('1') and len(phone) == 11 and phone.isdigit()):
                return jsonify({
                    "code": 400,
                    "error": "INVALID_PHONE",
                    "message": "手机号格式不正确"
                }), 400
            patient.Phone = phone or None  # 允许清空手机号

        db.session.commit()

        # 构建响应数据
        response_data = {
            "PatientID": patient.PatientID,
            "Name": patient.Name,
            "Gender": patient.Gender,
            "BirthDate": patient.BirthDate.strftime("%Y-%m-%d") if patient.BirthDate else None,
            "IdentityNo": patient.IdentityNo,  # 身份证号不可修改
            "Phone": patient.Phone
        }

        return jsonify({
            "code": 200,
            "data": response_data
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": f"更新失败: {str(e)}"
        }), 500

@bp.route('/patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        # 检查患者是否存在
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({
                "code": 404,
                "error": "PATIENT_NOT_FOUND",
                "message": "患者不存在"
            }), 404

        # 检查关联就诊记录
        visit_count = Visit.query.filter_by(PatientID=patient_id).count()
        # 检查关联住院记录
        admission_count = db.session.query(Admission) \
            .join(Visit, Visit.AdmissionID == Admission.AdmissionID) \
            .filter(Visit.PatientID == patient_id) \
            .count()

        if visit_count > 0 or admission_count > 0:
            return jsonify({
                "code": 400,
                "error": "HAS_RELATED_RECORDS",
                "message": "存在关联的就诊或住院记录，不可删除",
                "details": {
                    "relatedVisits": visit_count,
                    "relatedAdmissions": admission_count
                }
            }), 400

        # 执行删除
        db.session.delete(patient)
        db.session.commit()

        return jsonify({
            "code": 204,
            "finish": True
        }), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "SERVER_ERROR",
            "message": f"删除失败: {str(e)}"
        }), 500