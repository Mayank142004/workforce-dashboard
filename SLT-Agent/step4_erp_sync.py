import json
import requests
from datetime import datetime

from local_db import init_db, get_unsynced, mark_synced
from erp_api import create_checkin, create_timesheet

DEVICE_FILE = "storage/device.json"

def load_device():
    with open(DEVICE_FILE, "r") as f:
        return json.load(f)

def sync_to_erp(cookies):
    device = load_device()
    employee = device["employee_id"]

    session = requests.Session()
    for c in cookies:
        session.cookies.set(c["name"], c["value"], domain=c["domain"])

    unsynced = get_unsynced()
    if not unsynced:
        return

    for work_date, normal_sec, ot_sec in unsynced:
        hours = round(normal_sec / 3600, 2)
        ot_hours = round(ot_sec / 3600, 2)

        # Attendance
        create_checkin(
            session,
            employee,
            f"{work_date} 09:00:00",
            "IN"
        )
        create_checkin(
            session,
            employee,
            f"{work_date} 18:30:00",
            "OUT"
        )

        # Timesheet
        create_timesheet(
            session,
            employee,
            work_date,
            hours,
            ot_hours
        )

        mark_synced(work_date)
        print(f"✅ ERP synced for {work_date}")
