from datetime import datetime
from erp_client import erp_post

def mark_attendance(employee, date_str):
    payload = {
        "employee": employee,
        "attendance_date": date_str,
        "status": "Present"
    }

    r = erp_post("/api/resource/Attendance", payload)

    if r.status_code in (200, 201):
        return True
    else:
        print("Attendance error:", r.text)
        return False
