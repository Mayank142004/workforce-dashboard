import os
import sys
import time
import subprocess
import threading
import ctypes
from ctypes import wintypes

from config import STORAGE_PATH, ERP_SYNC_INTERVAL_MIN
from step1_login import start_login_ui
from step3_agent import SLTAgent
from step4_erp_push import run_erp_push

# 🆕 STARTUP REGISTER
from startup_register import ensure_startup_registered


# ==================================================
# SINGLE INSTANCE MUTEX (AGENT ONLY)
# ==================================================
MUTEX_NAME = "Global\\SLT_AGENT_BACKGROUND_MUTEX"

def is_another_agent_running():
    kernel32 = ctypes.windll.kernel32
    kernel32.CreateMutexW.restype = wintypes.HANDLE
    kernel32.GetLastError.restype = wintypes.DWORD

    kernel32.CreateMutexW(None, False, MUTEX_NAME)
    ERROR_ALREADY_EXISTS = 183
    return kernel32.GetLastError() == ERROR_ALREADY_EXISTS


# ==================================================
# ERP SYNC BACKGROUND THREAD
# ==================================================
def erp_sync_loop():
    print("🔁 ERP Sync thread started")

    while True:
        try:
            print("🔄 ERP Sync running...")
            run_erp_push()
        except Exception as e:
            print("❌ ERP Sync error (ignored):", e)

        time.sleep(ERP_SYNC_INTERVAL_MIN * 60)


# ==================================================
# AGENT MODE (BACKGROUND ONLY)
# ==================================================
def run_agent_mode():
    if is_another_agent_running():
        print("⚠️ SLT Agent already running. Exiting duplicate.")
        os._exit(0)

    print("🟢 SLT Agent started in BACKGROUND MODE")

    # 🧠 Start Agent (activity tracking)
    agent = SLTAgent()
    threading.Thread(target=agent.run, daemon=True).start()

    # 🔁 Start ERP Sync loop
    threading.Thread(target=erp_sync_loop, daemon=True).start()

    # 🔒 Keep process alive
    while True:
        time.sleep(60)


# ==================================================
# FORCE CLOSE LAUNCHER
# ==================================================
def auto_close_launcher(delay=100):
    def _close():
        time.sleep(delay)
        os._exit(0)
    threading.Thread(target=_close, daemon=True).start()


# ==================================================
# LAUNCHER MODE
# ==================================================
def run_launcher_mode():
    print("🚀 SLT Agent Launcher Started")

    # 🔐 First run → ERP login
    if not os.path.exists(STORAGE_PATH):
        print("🔐 First run → Opening ERP Login")
        start_login_ui()
    else:
        print("✅ Device already registered")

    # 🟢 Register startup
    try:
        ensure_startup_registered()
    except Exception as e:
        print("⚠️ Startup registration failed:", e)

    # 🚀 Start background agent
    try:
        exe_path = sys.executable
        exe_dir = os.path.dirname(exe_path)

        subprocess.Popen(
            [exe_path, "--agent"],
            cwd=exe_dir,
            creationflags=subprocess.DETACHED_PROCESS
        )

        print("✅ Background agent started")

    except Exception as e:
        print("❌ Failed to start agent:", e)

    auto_close_launcher(8)

    while True:
        time.sleep(1)


# ==================================================
# ENTRY POINT
# ==================================================
if __name__ == "__main__":
    if "--agent" in sys.argv:
        run_agent_mode()
    else:
        run_launcher_mode()
