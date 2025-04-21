from flask import jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from app.models.ward import Ward
from app.models.department import Department
from app.models.admission import Admission
from app.extensions import db
from app.models.patient import Patient
from app.models.visit import Visit


bp = Blueprint('ward', __name__)


@bp.route('/ward', methods=['GET'])
def get_wards():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        dept_id = request.args.get('deptId', type=int)
        floor = request.args.get('floor', type=int)

        if page < 1 or page_size < 1:
            return jsonify({
                "code": 400,
                "error": "分页参数必须大于0"
            }), 400

        query = db.session.query(Ward, Department.DeptName).join(Department, Ward.DeptID == Department.DeptID)

        if dept_id is not None:
            query = query.filter(Ward.DeptID == dept_id)
        if floor is not None:
            query = query.filter(Ward.Floor == floor)

        pagination = query.paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )

        wards_list = []
        for ward, dept_name in pagination.items:
            wards_list.append({
                "WardID": ward.WardID,
                "WardName": ward.WardName,
                "Floor": ward.Floor,
                "Capacity": ward.Capacity,
                "DeptID": ward.DeptID,
                "DeptName": dept_name 
            })

        return jsonify({
            "code": 200,
            "data": {
                "total": pagination.total,
                "page": pagination.page,
                "pageSize": page_size,
                "list": wards_list
            }
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

    
@bp.route('/ward', methods=['POST'])
def add_ward():
    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({
                "code": 415,
                "error": "INVALID_CONTENT_TYPE",
                "message": "必须使用 application/json 格式"
            }), 415

        data = request.get_json()
        if not data:
            return jsonify({
                "code": 400,
                "error": "EMPTY_REQUEST_BODY",
                "message": "请求体不能为空"
            }), 400

        errors = []
        
        ward_name = data.get('WardName', '').strip()
        if not ward_name:
            errors.append({"field": "WardName", "message": "病房名称不能为空"})
        elif len(ward_name) > 50:
            errors.append({"field": "WardName", "message": "病房名称长度不能超过50个字符"})

        try:
            floor = int(data.get('Floor'))
        except (TypeError, ValueError):
            errors.append({"field": "Floor", "message": "楼层必须为整数"})

        try:
            capacity = int(data.get('Capacity'))
            if capacity <= 0:
                errors.append({"field": "Capacity", "message": "床位容量必须大于0"})
        except (TypeError, ValueError):
            errors.append({"field": "Capacity", "message": "床位容量必须为整数"})

        try:
            dept_id = int(data.get('DeptID'))
        except (TypeError, ValueError):
            errors.append({"field": "DeptID", "message": "科室ID必须为整数"})
        else:
            department = Department.query.get(dept_id)
            if not department:
                return jsonify({
                    "code": 404,
                    "error": "DEPT_NOT_FOUND",
                    "message": "指定科室不存在"
                }), 404

        if errors:
            return jsonify({
                "code": 400,
                "error": "PARAM_VALIDATION_FAILED",
                "message": "参数验证失败",
                "details": errors
            }), 400
        
        max_ward_id = db.session.query(db.func.max(Ward.WardID)).scalar()  
        new_ward_id = max_ward_id + 1 if max_ward_id else 1  

        new_ward = Ward(
            WardID=new_ward_id,  
            WardName=ward_name,
            Floor=floor,
            Capacity=capacity,
            DeptID=dept_id
        )
        
        db.session.add(new_ward)
        db.session.commit()
        db.session.refresh(new_ward)

        return jsonify({
            "code": 201,
            "data": {
                "WardID": new_ward.WardID,
                "WardName": new_ward.WardName,
                "Floor": new_ward.Floor,
                "Capacity": new_ward.Capacity,
                "DeptID": new_ward.DeptID,
                "DeptName": department.DeptName
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "INTERNAL_SERVER_ERROR",
            "message": f"服务器内部错误: {str(e)}"
        }), 500


@bp.route('/ward/<int:ward_id>', methods=['GET'])
def get_ward_detail(ward_id):
    try:
        ward = Ward.query.get(ward_id)
        if not ward:
            return jsonify({
                "code": 404,
                "error": "病房不存在"
            }), 404

        department = Department.query.get(ward.DeptID)  

        admissions = db.session.query(Admission, Patient).join(
            Visit, Visit.AdmissionID == Admission.AdmissionID  
        ).join(
            Patient, Patient.PatientID == Visit.PatientID  
        ).filter(
            Admission.WardID == ward_id,
            Admission.DischargeDate == None  
        ).all()

        occupied = len(admissions)
        available = ward.Capacity - occupied

        bed_status = []
        for admission, patient in admissions:
            bed_status.append({
                "BedNo": admission.BedNo,
                "PatientID": patient.PatientID if patient else None,
                "PatientName": patient.Name if patient else "未知"
            })

        return jsonify({
            "code": 200,
            "data": {
                "WardID": ward.WardID,
                "WardName": ward.WardName,
                "Floor": ward.Floor,
                "Capacity": ward.Capacity,
                "DeptID": ward.DeptID,
                "DeptName": department.DeptName if department else "", 
                "OccupiedBeds": occupied,
                "AvailableBeds": available,
                "BedStatus": bed_status
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500


@bp.route('/ward/<int:ward_id>', methods=['PUT'])
def edit_ward(ward_id):
    try:
        ward = Ward.query.get(ward_id)
        if not ward:
            return jsonify({
                "code": 404,
                "error": "病房不存在"
            }), 404

        data = request.get_json()

        if "WardName" in data:
            ward.WardName = data["WardName"]
        if "Floor" in data:
            ward.Floor = data["Floor"]
        if "Capacity" in data:
            ward.Capacity = data["Capacity"]

        db.session.commit()

        department = Department.query.get(ward.DeptID)

        return jsonify({
            "code": 200,
            "data": {
                "WardID": ward.WardID,
                "WardName": ward.WardName,
                "Floor": ward.Floor,
                "Capacity": ward.Capacity,
                "DeptID": ward.DeptID,
                "DeptName": department.DeptName if department else ""  
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500


