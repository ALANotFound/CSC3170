from flask import jsonify, request, Blueprint
from app.extensions import db
from app.models.visit import Visit
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.admission import Admission
from datetime import datetime
from app.models.ward import Ward
from app.models.department import Department

bp = Blueprint('visit', __name__)

@bp.route('/visit', methods=['GET'])
def get_visits():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        patient_id = request.args.get('patientId', type=int)
        doctor_id = request.args.get('doctorId', type=int)
        start_date = request.args.get('startDate', type=str)
        end_date = request.args.get('endDate', type=str)

        if page < 1 or page_size < 1:
            return jsonify({
                "code": 400,
                "error": "分页参数必须大于0"
            }), 400

        query = db.session.query(
            Visit.VisitID, Visit.PatientID, Visit.DoctorID, Visit.AdmissionID,
            Visit.VisitDate, Visit.Complaint, Visit.Diagnosis, Visit.Prescription, Visit.Fee
        ).join(Patient, Visit.PatientID == Patient.PatientID).join(Doctor, Visit.DoctorID == Doctor.DoctorID)

        if patient_id is not None:
            query = query.filter(Visit.PatientID == patient_id)
        if doctor_id is not None:
            query = query.filter(Visit.DoctorID == doctor_id)
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Visit.VisitDate >= start_date_obj)
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "START_DATE_INVALID",
                    "message": "开始日期格式不正确，应该为 YYYY-MM-DD"
                }), 400
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                query = query.filter(Visit.VisitDate <= end_date_obj)
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "END_DATE_INVALID",
                    "message": "结束日期格式不正确，应该为 YYYY-MM-DD"
                }), 400

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        visits_list = []
        for visit in pagination.items:
            visits_list.append({
                "VisitID": visit.VisitID,
                "PatientID": visit.PatientID,
                "DoctorID": visit.DoctorID,
                "AdmissionID": visit.AdmissionID,
                "VisitDate": visit.VisitDate.strftime('%Y-%m-%d'),
                "Complaint": visit.Complaint,
                "Diagnosis": visit.Diagnosis,
                "Prescription": visit.Prescription,
                "Fee": float(visit.Fee) if visit.Fee is not None else None
            })

        return jsonify({
            "code": 200,
            "data": visits_list
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@bp.route('/visit', methods=['POST'])
def add_visit():
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
            patient_id = int(data.get('PatientID'))
        except (TypeError, ValueError):
            errors.append({"field": "PatientID", "message": "患者ID必须为整数"})
        
        try:
            doctor_id = int(data.get('DoctorID'))
        except (TypeError, ValueError):
            errors.append({"field": "DoctorID", "message": "医生ID必须为整数"})
        else:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                errors.append({"field": "DoctorID", "message": "指定的医生不存在"})

        admission_id = data.get('AdmissionID')
        if admission_id is not None:
            try:
                admission_id = int(admission_id)
            except (TypeError, ValueError):
                errors.append({"field": "AdmissionID", "message": "入院ID必须为整数"})
            else:
                admission = Admission.query.get(admission_id)
                if not admission:
                    errors.append({"field": "AdmissionID", "message": "指定的入院记录不存在"})

        visit_date = data.get('VisitDate', '').strip()
        if not visit_date:
            errors.append({"field": "VisitDate", "message": "就诊日期不能为空"})
        else:
            try:
                visit_date = datetime.strptime(visit_date, '%Y-%m-%d')
            except ValueError:
                errors.append({"field": "VisitDate", "message": "就诊日期格式不正确，应该为 YYYY-MM-DD"})

        complaint = data.get('Complaint', '').strip()
        if not complaint:
            errors.append({"field": "Complaint", "message": "主诉不能为空"})

        diagnosis = data.get('Diagnosis', '').strip()
        if not diagnosis:
            errors.append({"field": "Diagnosis", "message": "诊断不能为空"})

        prescription = data.get('Prescription', '').strip()
        if not prescription:
            errors.append({"field": "Prescription", "message": "处方不能为空"})

        try:
            fee = float(data.get('Fee'))
            if fee <= 0:
                errors.append({"field": "Fee", "message": "费用必须大于0"})
        except (TypeError, ValueError):
            errors.append({"field": "Fee", "message": "费用必须为正数"})

        if errors:
            return jsonify({
                "code": 400,
                "error": "PARAM_VALIDATION_FAILED",
                "message": "参数验证失败",
                "details": errors
            }), 400

        max_visit_id = db.session.query(db.func.max(Visit.VisitID)).scalar()  
        new_visit_id = max_visit_id + 1 if max_visit_id else 1  


        new_visit = Visit(
            VisitID=new_visit_id,
            PatientID=patient_id,
            DoctorID=doctor_id,
            AdmissionID=admission_id if admission_id else None,
            VisitDate=visit_date,
            Complaint=complaint,
            Diagnosis=diagnosis,
            Prescription=prescription,
            Fee=fee
        )
        
        db.session.add(new_visit)
        db.session.commit()
        db.session.refresh(new_visit)

        patient = Patient.query.get(patient_id)
        doctor = Doctor.query.get(doctor_id)
        admission = Admission.query.get(admission_id) if admission_id else None

        return jsonify({
            "code": 201,
            "data": {
                "VisitID": new_visit.VisitID,
                "PatientID": new_visit.PatientID,
                "DoctorID": new_visit.DoctorID,
                "AdmissionID": new_visit.AdmissionID,
                "VisitDate": new_visit.VisitDate.strftime('%Y-%m-%d'),
                "Complaint": new_visit.Complaint,
                "Diagnosis": new_visit.Diagnosis,
                "Prescription": new_visit.Prescription,
                "Fee": float(new_visit.Fee)
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "INTERNAL_SERVER_ERROR",
            "message": f"服务器内部错误: {str(e)}"
        }), 500
    


@bp.route('/visit/<int:visit_id>', methods=['GET'])
def check_visit(visit_id):
    try:
        visit = Visit.query.get(visit_id)

        if not visit:
            return jsonify({
                "code": 404,
                "error": "就诊记录不存在"
            }), 404

        return jsonify({
            "code": 200,
            "data": {
                "VisitID": visit.VisitID,
                "PatientID": visit.PatientID,
                "DoctorID": visit.DoctorID,
                "AdmissionID": visit.AdmissionID,
                "VisitDate": visit.VisitDate.strftime('%Y-%m-%d'), 
                "Complaint": visit.Complaint,
                "Diagnosis": visit.Diagnosis,
                "Prescription": visit.Prescription,
                "Fee": float(visit.Fee) if visit.Fee is not None else None
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@bp.route('/visit/<int:visit_id>/prescription', methods=['PUT'])
def edit_prescription(visit_id):
    try:
     
        visit = Visit.query.get(visit_id)

        if not visit:
            return jsonify({
                "code": 404,
                "error": "就诊记录不存在"
            }), 404

        data = request.get_json()
        prescription = data.get("Prescription")

        if not prescription:
            return jsonify({
                "code": 400,
                "error": "Prescription 字段是必需的"
            }), 400

        visit.Prescription = prescription
        db.session.commit()  

        return jsonify({
            "code": 200,
            "data": {
                "VisitID": visit.VisitID,
                "PatientID": visit.PatientID,
                "DoctorID": visit.DoctorID,
                "AdmissionID": visit.AdmissionID,
                "VisitDate": visit.VisitDate.strftime('%Y-%m-%d'),  
                "Complaint": visit.Complaint,
                "Diagnosis": visit.Diagnosis,
                "Prescription": visit.Prescription,
                "Fee": float(visit.Fee)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500
