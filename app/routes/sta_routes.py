from flask import jsonify, request, Blueprint

bp = Blueprint('sta', __name__)

from flask import jsonify, request
from datetime import datetime
from sqlalchemy import func
from app.models.admission import Admission
from app.models.visit import Visit
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.ward import Ward
from app.extensions import db
from sqlalchemy.sql import extract

@bp.route('/department/<int:dept_id>/stats', methods=['GET'])
def department_stats(dept_id):
    try:
        start_date_str = request.args.get('startDate')
        end_date_str = request.args.get('endDate')

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "startDate 格式不正确，应该是 'YYYY-MM-DD'"
                }), 400
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "endDate 格式不正确，应该是 'YYYY-MM-DD'"
                }), 400
        else:
            end_date = None

        department = Department.query.get(dept_id)
        if not department:
            return jsonify({
                "code": 404,
                "error": f"DeptID {dept_id} 未找到"
            }), 404

        outpatient_count = db.session.query(func.count(Visit.VisitID)).join(Doctor).filter(Doctor.DeptID == dept_id)

        if start_date:
            outpatient_count = outpatient_count.filter(Visit.VisitDate >= start_date)
        if end_date:
            outpatient_count = outpatient_count.filter(Visit.VisitDate <= end_date)

        outpatient_count = outpatient_count.scalar()

        inpatient_count = db.session.query(func.count(Admission.AdmissionID)).filter(Admission.WardID.in_(
            db.session.query(Ward.WardID).filter(Ward.DeptID == dept_id)
        )).filter(Admission.DischargeDate.is_(None)) 

        if start_date:
            inpatient_count = inpatient_count.filter(Admission.AdmissionDate >= start_date)
        if end_date:
            inpatient_count = inpatient_count.filter(Admission.AdmissionDate <= end_date)

        inpatient_count = inpatient_count.scalar()

        total_revenue = db.session.query(func.sum(Visit.Fee)).join(Doctor).filter(Doctor.DeptID == dept_id)

        if start_date:
            total_revenue = total_revenue.filter(Visit.VisitDate >= start_date)
        if end_date:
            total_revenue = total_revenue.filter(Visit.VisitDate <= end_date)

        total_revenue = total_revenue.scalar() or 0 

        return jsonify({
            "code": 200,
            "data": [
                {
                    "DeptID": department.DeptID,
                    "DeptName": department.DeptName,
                    "outpatientCount": outpatient_count,
                    "inpatientCount": inpatient_count,
                    "totalRevenue": int(total_revenue)
                }
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500
    

@bp.route('/report/revenue', methods=['GET'])
def revenue_stats():
    try:
        start_date_str = request.args.get('startDate')
        end_date_str = request.args.get('endDate')

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "startDate 格式不正确，应该是 'YYYY-MM-DD'"
                }), 400
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "endDate 格式不正确，应该是 'YYYY-MM-DD'"
                }), 400
        else:
            end_date = None

        revenue_query = db.session.query(
            extract('year', Visit.VisitDate).label('Year'),
            extract('month', Visit.VisitDate).label('Month'),
            func.sum(Visit.Fee).label('Revenue')
        ).group_by('Year', 'Month')

        if start_date:
            revenue_query = revenue_query.filter(Visit.VisitDate >= start_date)
        if end_date:
            revenue_query = revenue_query.filter(Visit.VisitDate <= end_date)

        revenue_details = revenue_query.all()

        total_revenue = int(sum([revenue.Revenue for revenue in revenue_details]))

        details = [
            {
                "Period": f"{int(revenue.Year)}-{int(revenue.Month):02d}",
                "Revenue": float(revenue.Revenue) if revenue.Revenue else 0.0
            }
            for revenue in revenue_details
        ]

        return jsonify({
            "code": 200,
            "data": {
                "Total": total_revenue,
                "Details": details
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@bp.route('/doctor/<int:doctor_id>/workload', methods=['GET'])
def doctor_workload(doctor_id):
    try:
        start_date_str = request.args.get('startDate')
        end_date_str = request.args.get('endDate')

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "startDate 格式不正确，应该是 'YYYY-MM-DD'"
                }), 400
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    "code": 400,
                    "error": "endDate 格式不正确，应该是 'YYYY-MM-DD'"
                }), 400
        else:
            end_date = None

        doctor_info = db.session.query(Doctor).filter(Doctor.DoctorID == doctor_id).first()
        if not doctor_info:
            return jsonify({
                "code": 404,
                "error": f"Doctor with ID {doctor_id} not found"
            }), 404

        visit_query = db.session.query(Visit).filter(Visit.DoctorID == doctor_id)

        if start_date:
            visit_query = visit_query.filter(Visit.VisitDate >= start_date)
        if end_date:
            visit_query = visit_query.filter(Visit.VisitDate <= end_date)

        visits = visit_query.all()

        visit_count = len(visits)  
        admission_count = len(set([visit.AdmissionID for visit in visits if visit.AdmissionID]))
        total_patients = len(set([visit.PatientID for visit in visits])) 

        return jsonify({
            "code": 200,
            "data": {
                "DoctorID": doctor_info.DoctorID,
                "Name": doctor_info.Name,
                "visitCount": visit_count,
                "admissionCount": admission_count,
                "totalPatients": total_patients
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"服务器内部错误: {str(e)}"
        }), 500
