from datetime import datetime
from erp_client import erp_post

def create_timesheet(employee, from_time, to_time, hours):
    payload = {
        "employee": employee,
        "time_logs": [
            {
                "from_time": from_time,
                "to_time": to_time,
                "hours": hours
            }
        ]
    }

    r = erp_post("/api/resource/Timesheet", payload)

    if r.status_code in (200, 201):
        return True
    else:
        print("Timesheet error:", r.text)
        return False
