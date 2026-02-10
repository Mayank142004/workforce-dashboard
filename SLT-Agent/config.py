import os
from dotenv import load_dotenv


# ===============================
# SLT Agent - Global Configuration
# ===============================

APP_NAME = "SLT-Agent"

# ==================================================
# ERP DETAILS
# ==================================================
ERP_BASE_URL = "https://erp.sltechsoft.com"
ERP_LOGIN_URL = "https://erp.sltechsoft.com/login"

# 🔐 AGENT API USER (Background sync only)
# ⚠️ Production me env variable use karna recommended
ERP_API_KEY = os.getenv("ERP_API_KEY_ENV")
ERP_API_SECRET = os.getenv("ERP_API_SECRET_ENV")

# Login success detect
SUCCESS_REDIRECT_KEYWORDS = [
    "/app",
    "/app/home",
    "/desk"
]

# ==================================================
# ✅ SAFE WINDOWS STORAGE (EXE SAFE)
# ==================================================
BASE_DIR = os.path.join(
    os.environ.get("LOCALAPPDATA", os.getcwd()),
    APP_NAME
)

STORAGE_DIR = os.path.join(BASE_DIR, "storage")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
LOG_DIR = os.path.join(BASE_DIR, "activity_logs")

DEVICE_FILE = "device.json"
DB_FILE = "local.db"

STORAGE_PATH = os.path.join(STORAGE_DIR, DEVICE_FILE)
DB_PATH = os.path.join(STORAGE_DIR, DB_FILE)

# Auto-create folders
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ==================================================
# 🕘 WORK POLICY (FLEXIBLE)
# ==================================================
# Office window (soft window – late/early allowed)
OFFICE_START_HOUR = 9          # reference only
OFFICE_END_HOUR = 20           # reference only

# Core rules
NORMAL_WORK_HOURS = 8          # hours
MAX_OVERTIME_HOURS = 4         # hours

# ==================================================
# 💤 IDLE / BREAK POLICY
# ==================================================
IDLE_TIME_MIN = 20             # >=20 min → STOP work count

LUNCH_DURATION_MIN = 60        # auto-detect (once/day)
BREAK_DURATION_MIN = 15        # auto-detect
MAX_BREAKS_PER_DAY = 2

# ==================================================
# 📸 SCREENSHOT POLICY
# ==================================================
SCREENSHOT_INTERVAL_MIN = 10   # every 10 min
SCREENSHOT_DURING_OVERTIME = True

# Screenshot ONLY when:
# - idle < 20 min
# - active work time

# ==================================================
# 🔁 ERP SYNC POLICY
# ==================================================
ERP_SYNC_INTERVAL_MIN = 10     # 🔥 AUTO PUSH every 10 minutes

# ERP behavior:
# - Check-IN → once per day (first_seen)
# - Check-OUT → overwrite (last_seen)
# - Timesheet → create once, update hours
# - Attendance → later phase (from Checkin)

# ==================================================
# 🐞 DEBUG
# ==================================================
DEBUG = True
