import time
from datetime import datetime, date

from activity_tracker import ActivityTracker
from state_manager import DailyState
from config import *

from local_db import init_db, save_day
from step5_screenshot import take_screenshot
from activity_logger import log_activity
from step4_erp_push import run_erp_push   # CLOSED DAY ONLY


# ==================================================
# CONSTANTS
# ==================================================
IDLE_LIMIT_SEC   = IDLE_TIME_MIN * 60     # 20 min
BREAK_SEC        = BREAK_DURATION_MIN * 60
LUNCH_SEC        = LUNCH_DURATION_MIN * 60

NORMAL_LIMIT_SEC = NORMAL_WORK_HOURS * 3600
MAX_OT_SEC       = MAX_OVERTIME_HOURS * 3600


# ==================================================
# SLT BACKGROUND AGENT (HUBSTAFF EXACT MODE)
# ==================================================
class SLTAgent:
    def __init__(self):
        print("🧠 SLT Agent started (Hubstaff 20-min Idle Rule)")

        self.state = DailyState()
        self.tracker = ActivityTracker()

        init_db()

        self.idle_seconds = 0
        self.last_screenshot_min = None
        self.last_idle_bucket = None

    # ------------------------------------------------
    # IDLE HANDLING (LUNCH / BREAK AUTO-DETECT)
    # ------------------------------------------------
    def handle_idle(self, idle_sec):
        bucket = int(idle_sec // 60)
        if bucket == self.last_idle_bucket:
            return

        self.last_idle_bucket = bucket

        if idle_sec >= LUNCH_SEC and not self.state.lunch_used:
            self.state.lunch_used = True
            print("🍽 Lunch detected")
            return

        if idle_sec >= BREAK_SEC and self.state.breaks_used < MAX_BREAKS_PER_DAY:
            self.state.breaks_used += 1
            print(f"☕ Break detected ({self.state.breaks_used})")
            return

    # ------------------------------------------------
    # ADD WORK (NORMAL + OT)
    # ------------------------------------------------
    def add_work(self, sec):
        if self.state.normal_seconds < NORMAL_LIMIT_SEC:
            used = min(sec, NORMAL_LIMIT_SEC - self.state.normal_seconds)
            self.state.normal_seconds += used
            sec -= used

        if sec > 0 and self.state.ot_seconds < MAX_OT_SEC:
            self.state.ot_seconds += min(sec, MAX_OT_SEC - self.state.ot_seconds)

    # ------------------------------------------------
    def day_changed(self):
        return self.state.date != date.today()

    # ------------------------------------------------
    def close_day(self):
        print("🌙 Day closed → save local + ERP sync")

        save_day(
            str(self.state.date),
            self.state.normal_seconds,
            self.state.ot_seconds,
            self.state.first_seen,
            self.state.last_seen
        )

        run_erp_push()

        self.state.reset()
        self.tracker.reset()

        self.idle_seconds = 0
        self.last_screenshot_min = None
        self.last_idle_bucket = None

    # ------------------------------------------------
    # SCREENSHOT (ONLY WHEN ACTIVE)
    # ------------------------------------------------
    def handle_screenshot(self, now, idle_sec):
        if idle_sec >= IDLE_LIMIT_SEC:
            return

        if self.state.lunch_used:
            return

        if not SCREENSHOT_DURING_OVERTIME and self.state.normal_seconds >= NORMAL_LIMIT_SEC:
            return

        if now.minute % SCREENSHOT_INTERVAL_MIN != 0:
            return

        if self.last_screenshot_min == now.minute:
            return

        self.last_screenshot_min = now.minute
        take_screenshot()

    # ------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------
    def run(self):
        print("🚀 SLT Agent running in background")
        self.tracker.start()   # ONLY ONCE

        while True:
            try:
                now = datetime.now()

                # ---- DAY CHANGE ----
                if self.day_changed():
                    self.close_day()

                idle_sec = (now - self.tracker.last_input_time).total_seconds()

                # ---- IDLE TRACK ----
                if idle_sec >= 60:
                    self.idle_seconds += 60
                else:
                    self.idle_seconds = 0

                    if not self.state.first_seen:
                        self.state.first_seen = now
                    self.state.last_seen = now
                    self.last_idle_bucket = None

                # ---- IDLE >= 20 MIN ----
                if self.idle_seconds >= IDLE_LIMIT_SEC:
                    self.handle_idle(self.idle_seconds)

                # ---- COUNT WORK ONLY IF NOT IDLE ----
                if idle_sec < IDLE_LIMIT_SEC and not self.state.lunch_used:
                    self.add_work(60)

                self.handle_screenshot(now, idle_sec)
                log_activity(self.state, idle_sec)

                save_day(
                    str(self.state.date),
                    self.state.normal_seconds,
                    self.state.ot_seconds,
                    self.state.first_seen,
                    self.state.last_seen
                )

                time.sleep(60)

            except Exception as e:
                print("❌ Agent error:", e)
                time.sleep(10)


# ==================================================
if __name__ == "__main__":
    SLTAgent().run()
