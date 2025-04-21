from flask import jsonify, request, Blueprint
from app.extensions import db
from app.models.ward import Ward
from app.models.admission import Admission
from datetime import datetime
from app.models.patient import Patient
from app.models.visit import Visit

bp = Blueprint('admission', __name__)

@bp.route('/admission', methods=['POST'])
def add_admission():
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
        
        try:
            ward_id = int(data.get('WardID'))
        except (TypeError, ValueError):
            errors.append({"field": "WardID", "message": "病区ID必须为整数"})
        
        bed_no = data.get('BedNo', '').strip()
        if not bed_no:
            errors.append({"field": "BedNo", "message": "床号不能为空"})
        
        admission_date = data.get('AdmissionDate', '').strip()
        if not admission_date:
            errors.append({"field": "AdmissionDate", "message": "入院日期不能为空"})
        else:
            try:
                admission_date = datetime.strptime(admission_date, '%Y-%m-%d')
            except ValueError:
                errors.append({"field": "AdmissionDate", "message": "入院日期格式不正确，应该为 YYYY-MM-DD"})

        admission_reason = data.get('AdmissionReason', '').strip()
        if not admission_reason:
            errors.append({"field": "AdmissionReason", "message": "入院原因不能为空"})

        if errors:
            return jsonify({
                "code": 400,
                "error": "PARAM_VALIDATION_FAILED",
                "message": "参数验证失败",
                "details": errors
            }), 400

        max_admission_id = db.session.query(db.func.max(Admission.AdmissionID)).scalar()  
        new_admission_id = max_admission_id + 1 if max_admission_id else 1  

        new_admission = Admission(
            AdmissionID=new_admission_id,
            WardID=ward_id,
            BedNo=bed_no,
            AdmissionDate=admission_date,
            AdmissionReason=admission_reason
        )
        
        db.session.add(new_admission)
        db.session.commit()
        db.session.refresh(new_admission)

        return jsonify({
            "AdmissionID": new_admission_id,
            "WardID": new_admission.WardID,
            "VisitID": data.get('VisitID'),  
            "BedNo": new_admission.BedNo,
            "AdmissionDate": new_admission.AdmissionDate.strftime('%Y-%m-%d'),
            "AdmissionReason": new_admission.AdmissionReason
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "INTERNAL_SERVER_ERROR",
            "message": f"服务器内部错误: {str(e)}"
        }), 500

from datetime import datetime
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

@bp.route('/admission/<int:admission_id>/discharge', methods=['PUT'])
def discharge_patient(admission_id):
    try:
        data = request.get_json()
        discharge_date_str = data.get('DischargeDate')

        if not discharge_date_str:
            return jsonify({
                "code": 400,
                "error": "DischargeDate 参数是必需的"
            }), 400

        try:
            discharge_date = datetime.strptime(discharge_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                "code": 400,
                "error": "DischargeDate 格式不正确，应该是 'YYYY-MM-DD'"
            }), 400

        admission = Admission.query.get(admission_id)
        if not admission:
            return jsonify({
                "code": 404,
                "error": f"AdmissionID {admission_id} 未找到"
            }), 404

        if discharge_date < admission.AdmissionDate:
            return jsonify({
                "code": 400,
                "error": "DischargeDate 不能早于 AdmissionDate"
            }), 400

        admission.DischargeDate = discharge_date
        db.session.commit()

        visit = Visit.query.filter_by(AdmissionID=admission_id).first()
        if visit:
            visit_id = visit.VisitID
        else:
            visit_id = None


        return jsonify({
            
            "AdmissionID": admission.AdmissionID,          
            "WardID": admission.WardID,                    
            "VisitID": visit_id if visit_id else None,    
            "BedNo": admission.BedNo,                      
            "AdmissionDate": admission.AdmissionDate.strftime('%Y-%m-%d'),  
            "DischargeDate": admission.DischargeDate.strftime('%Y-%m-%d'), 
            "AdmissionReason": admission.AdmissionReason  
        })

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": f"数据库错误: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500


@bp.route('/admission/active', methods=['GET'])
def check_current_patients():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        ward_id = request.args.get('wardId', type=int)
        dept_id = request.args.get('DeptId', type=int)

        if page < 1 or page_size < 1:
            return jsonify({
                "code": 400,
                "error": "分页参数必须大于0"
            }), 400

        query = db.session.query(
            Admission.AdmissionID, Patient.PatientID, Patient.Name.label('PatientName'),
            Admission.WardID, Admission.BedNo, Admission.AdmissionDate
        ).join(Patient, Admission.AdmissionID == Patient.PatientID)  

        query = query.filter(Admission.DischargeDate.is_(None))

        if ward_id is not None:
            query = query.filter(Admission.WardID == ward_id)
        if dept_id is not None:
            query = query.join(Ward, Admission.WardID == Ward.WardID).filter(Ward.DeptID == dept_id)

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        active_patients_list = []
        for admission in pagination.items:
            active_patients_list.append({
                "AdmissionID": admission.AdmissionID,
                "PatientID": admission.PatientID,  
                "PatientName": admission.PatientName,
                "WardID": admission.WardID,
                "BedNo": admission.BedNo,
                "AdmissionDate": admission.AdmissionDate.strftime('%Y-%m-%d')
            })

        return jsonify({
            "code": 200,
            "data": {
                "total": pagination.total,
                "page": pagination.page,
                "pageSize": page_size,
                "list": active_patients_list
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500
