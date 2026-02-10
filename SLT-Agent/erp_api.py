import requests
from config import ERP_BASE_URL

# =====================================================
# AUTH / SESSION HELPERS
# =====================================================

def get_logged_user(session: requests.Session):
    """
    Returns logged-in user email from ERPNext session
    """
    url = f"{ERP_BASE_URL}/api/method/frappe.auth.get_logged_user"
    r = session.get(url)

    if r.status_code == 200:
        return r.json().get("message")

    return None


def get_employee_by_email(session: requests.Session, email: str):
    """
    Fetch Employee record using user_id (email)
    """
    url = f"{ERP_BASE_URL}/api/resource/Employee"
    params = {
        "filters": f'[["user_id","=","{email}"]]',
        "fields": '["name","employee_name","department","designation","status"]'
    }

    r = session.get(url, params=params)

    if r.status_code == 200:
        data = r.json().get("data", [])
        return data[0] if data else None

    return None


# =====================================================
# ATTENDANCE (CHECK-IN / CHECK-OUT)
# =====================================================

def create_checkin(session: requests.Session, employee: str, time_str: str, log_type: str):
    """
    Create Employee Checkin (IN / OUT)
    """
    url = f"{ERP_BASE_URL}/api/resource/Employee Checkin"

    payload = {
        "employee": employee,
        "time": time_str,
        "log_type": log_type,
        "source": "SLT Agent"
    }

    r = session.post(url, json=payload)

    if r.status_code not in (200, 201):
        print("❌ Checkin failed:", r.text)
        return False

    return True


# =====================================================
# TIMESHEET (NORMAL + OT)
# =====================================================

def create_timesheet(
    session: requests.Session,
    employee: str,
    work_date: str,
    normal_hours: float,
    ot_hours: float
):
    """
    Create Timesheet with Normal + Overtime hours
    """
    url = f"{ERP_BASE_URL}/api/resource/Timesheet"

    time_logs = []

    if normal_hours > 0:
        time_logs.append({
            "activity_type": "Work",
            "hours": normal_hours
        })

    if ot_hours > 0:
        time_logs.append({
            "activity_type": "Overtime",
            "hours": ot_hours
        })

    payload = {
        "employee": employee,
        "start_date": work_date,
        "end_date": work_date,
        "time_logs": time_logs
    }

    r = session.post(url, json=payload)

    if r.status_code not in (200, 201):
        print("❌ Timesheet failed:", r.text)
        return False

    return True
