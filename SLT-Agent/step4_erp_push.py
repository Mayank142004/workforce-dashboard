import json
import sqlite3
from datetime import datetime, date

from config import DB_PATH, STORAGE_PATH
from erp_client import erp_get, erp_post, erp_put


# ==================================================
# HELPERS
# ==================================================

def get_employee():
    with open(STORAGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["employee_id"]


def safe_dt(dt):
    if not dt:
        return None
    return dt if isinstance(dt, str) else dt.strftime("%Y-%m-%d %H:%M:%S")


# ==================================================
# ERP LOOKUPS
# ==================================================

def get_checkin(employee, log_type, work_date):
    res = erp_get(
        "/api/resource/Employee Checkin",
        params={
            "filters": json.dumps([
                ["employee", "=", employee],
                ["log_type", "=", log_type],
                ["time", ">=", f"{work_date} 00:00:00"],
                ["time", "<=", f"{work_date} 23:59:59"]
            ]),
            "order_by": "time desc",
            "limit": 1
        }
    )
    return res["data"][0] if res and res.get("data") else None


def get_timesheet(employee, work_date):
    res = erp_get(
        "/api/resource/Timesheet",
        params={
            "filters": json.dumps([
                ["employee", "=", employee],
                ["start_date", "=", work_date]
            ]),
            "limit": 1
        }
    )
    return res["data"][0] if res and res.get("data") else None


# ==================================================
# CHECKIN / CHECKOUT (SMART UPSERT)
# ==================================================

def sync_checkins(employee, work_date, first_seen, last_seen):
    if not first_seen or not last_seen:
        print(f"⚠️ Checkin skipped ({work_date}) – missing time")
        return

    print(f"▶ Sync Checkin: {work_date}")

    first_seen = safe_dt(first_seen)
    last_seen = safe_dt(last_seen)

    # -------- IN (CREATE ONCE) --------
    in_row = get_checkin(employee, "IN", work_date)
    if not in_row:
        erp_post("/api/resource/Employee Checkin", {
            "employee": employee,
            "log_type": "IN",
            "time": first_seen
        })
        print("✔ IN created:", first_seen)

    # -------- OUT (ALWAYS UPDATE) --------
    out_row = get_checkin(employee, "OUT", work_date)
    if not out_row:
        erp_post("/api/resource/Employee Checkin", {
            "employee": employee,
            "log_type": "OUT",
            "time": last_seen
        })
        print("✔ OUT created:", last_seen)
    else:
        erp_put(
            f"/api/resource/Employee Checkin/{out_row['name']}",
            {"time": last_seen}
        )
        print("🔄 OUT updated:", last_seen)


# ==================================================
# TIMESHEET (HUBSTAFF-STRICT, ERP-SAFE)
# ==================================================

def sync_timesheet(employee, work_date, first_seen, last_seen, normal_sec, ot_sec):
    if not first_seen or not last_seen:
        print(f"⚠️ Timesheet skipped ({work_date}) – missing time")
        return

    total_hours = round((normal_sec + ot_sec) / 3600, 2)
    first_seen = safe_dt(first_seen)

    ts = get_timesheet(employee, work_date)

    # ⚠️ IMPORTANT:
    # We intentionally DO NOT send to_time
    # ERPNext will otherwise recalculate hours incorrectly
    payload = {
        "employee": employee,
        "start_date": work_date,
        "time_logs": [{
            "from_time": first_seen,
            "hours": total_hours,
            "activity_type": "Working"
        }]
    }

    if not ts:
        erp_post("/api/resource/Timesheet", payload)
        print(f"✔ Timesheet created ({total_hours} hrs)")
    else:
        # NOTE: overwriting time_logs intentionally (daily aggregate model)
        erp_put(f"/api/resource/Timesheet/{ts['name']}", payload)
        print(f"🔄 Timesheet updated ({total_hours} hrs)")


# ==================================================
# MAIN SYNC ENGINE (🔥 CLOSED DAYS ONLY)
# ==================================================

def run_erp_push():
    print("=" * 60)
    print(" ERP AUTO SYNC STARTED ", datetime.now())
    print("=" * 60)

    employee = get_employee()
    today = date.today().isoformat()

    db = sqlite3.connect(DB_PATH)
    rows = db.execute("""
        SELECT
            work_date,
            normal_seconds,
            ot_seconds,
            first_seen,
            last_seen
        FROM daily_work
        WHERE first_seen IS NOT NULL
          AND last_seen IS NOT NULL
          AND work_date < ?
    """, (today,)).fetchall()
    db.close()

    print(f"📊 Closed days found: {len(rows)}")

    for work_date, normal_sec, ot_sec, first_seen, last_seen in rows:
        try:
            sync_checkins(employee, work_date, first_seen, last_seen)
            sync_timesheet(
                employee,
                work_date,
                first_seen,
                last_seen,
                normal_sec,
                ot_sec
            )
        except Exception as e:
            print("⚠️ ERP sync failed for", work_date, ":", e)

    print("=" * 60)
    print(" ERP AUTO SYNC COMPLETED ")
    print("=" * 60)


# ==================================================
if __name__ == "__main__":
    run_erp_push()
