import os
import sys
import winreg

APP_NAME = "SLT-Agent"

def ensure_startup_registered():
    try:
        exe_path = sys.executable

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(
            key,
            APP_NAME,
            0,
            winreg.REG_SZ,
            exe_path
        )

        winreg.CloseKey(key)

        print("✅ Startup registered (User level, no admin)")

    except Exception as e:
        print("❌ Failed to register startup:", e)
