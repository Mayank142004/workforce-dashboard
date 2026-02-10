import json
import os
from datetime import datetime
from config import LOG_DIR

LOG_FILE = os.path.join(LOG_DIR, "activity.json")

def log_activity(state, idle_sec):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "normal_hours": round(state.normal_seconds / 3600, 2),
        "ot_hours": round(state.ot_seconds / 3600, 2),
        "idle_seconds": int(idle_sec),
        "lunch_used": state.lunch_used,
        "breaks_used": state.breaks_used
    }

    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
