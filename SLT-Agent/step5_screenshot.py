import os
from datetime import datetime
import pyautogui
from config import SCREENSHOT_DIR

def take_screenshot():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SCREENSHOT_DIR, f"{ts}.png")
    pyautogui.screenshot(path)
