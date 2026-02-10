from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import glob

app = FastAPI(title="Workforce Tracking API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path configurations - UPDATE THESE TO YOUR ACTUAL PATHS
STORAGE_PATH = Path("C:\\Users\\Mayank\\AppData\\Local\\SLT-Agent\\storage")  # Adjust to your agent storage path
ACTIVITY_LOGS_PATH = Path("C:\\Users\\Mayank\\AppData\\Local\\SLT-Agent\\activity_logs")
SCREENSHOTS_PATH = Path("C:\\Users\\Mayank\\AppData\\Local\\SLT-Agent\\storage\\screenshots")
DEVICE_INFO_PATH = STORAGE_PATH / "device.json"

# Helper functions
def load_device_info() -> Dict[str, Any]:
    """Load employee device information"""
    try:
        with open(DEVICE_INFO_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "employee_id": "N/A",
            "employee_name": "Unknown",
            "email": "N/A",
            "department": "N/A",
            "designation": "N/A",
            "device_id": "N/A"
        }

def load_activity_log(date: str) -> List[Dict[str, Any]]:
    """Load activity log for a specific date"""
    log_file = ACTIVITY_LOGS_PATH / f"{date}.json"
    try:
        with open(log_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def calculate_daily_stats(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate daily statistics from activity logs"""
    if not activities:
        return {
            "total_work_hours": 0,
            "total_active_minutes": 0,
            "total_idle_minutes": 0,
            "sessions": 0,
            "first_login": None,
            "last_activity": None,
            "breaks_taken": 0,
            "lunch_taken": False
        }
    
    # Calculate total work time (max normal_hours from all sessions)
    sessions = []
    current_session = []
    
    for i, activity in enumerate(activities):
        # Detect session restart (when normal_hours resets)
        if i > 0 and activity['normal_hours'] < activities[i-1]['normal_hours']:
            if current_session:
                sessions.append(current_session)
            current_session = [activity]
        else:
            current_session.append(activity)
    
    if current_session:
        sessions.append(current_session)
    
    # Calculate stats
    total_work_hours = sum(max(s, key=lambda x: x['normal_hours'])['normal_hours'] for s in sessions)
    total_idle_seconds = sum(a['idle_seconds'] for a in activities)
    total_active_seconds = (total_work_hours * 3600) - total_idle_seconds
    
    first_timestamp = datetime.fromisoformat(activities[0]['timestamp'])
    last_timestamp = datetime.fromisoformat(activities[-1]['timestamp'])
    
    lunch_taken = any(a['lunch_used'] for a in activities)
    max_breaks = max((a['breaks_used'] for a in activities), default=0)
    
    return {
        "total_work_hours": round(total_work_hours, 2),
        "total_active_minutes": round(total_active_seconds / 60, 2),
        "total_idle_minutes": round(total_idle_seconds / 60, 2),
        "sessions": len(sessions),
        "first_login": first_timestamp.strftime("%H:%M"),
        "last_activity": last_timestamp.strftime("%H:%M"),
        "breaks_taken": max_breaks,
        "lunch_taken": lunch_taken
    }

# API Endpoints

@app.get("/")
def root():
    return {"message": "Workforce Tracking API", "version": "1.0.0"}

@app.get("/employee/info")
def get_employee_info():
    """Get employee device information"""
    return load_device_info()

@app.get("/work/today")
def get_today_stats():
    """Get today's work statistics"""
    today = datetime.now().strftime("%Y-%m-%d")
    activities = load_activity_log(today)
    
    if not activities:
        return {
            "date": today,
            "message": "No activity logged today",
            "stats": calculate_daily_stats([])
        }
    
    stats = calculate_daily_stats(activities)
    
    return {
        "date": today,
        "stats": stats,
        "employee": load_device_info()
    }

@app.get("/work/timesheet")
def get_timesheet(days: int = 7):
    """Get timesheet for the last N days"""
    end_date = datetime.now()
    timesheet = []
    
    for i in range(days):
        date = end_date - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        activities = load_activity_log(date_str)
        
        stats = calculate_daily_stats(activities)
        timesheet.append({
            "date": date_str,
            "day": date.strftime("%A"),
            "stats": stats
        })
    
    return {
        "period": f"Last {days} days",
        "timesheet": timesheet,
        "employee": load_device_info()
    }

@app.get("/activity/detailed")
def get_detailed_activity(date: str = None):
    """Get detailed activity log for a specific date"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    activities = load_activity_log(date)
    
    if not activities:
        raise HTTPException(status_code=404, detail=f"No activity found for {date}")
    
    return {
        "date": date,
        "total_entries": len(activities),
        "activities": activities,
        "stats": calculate_daily_stats(activities)
    }

@app.get("/screenshots/list")
def list_screenshots(date: str = None):
    """List available screenshots for a date"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    screenshot_dir = SCREENSHOTS_PATH / date
    
    if not screenshot_dir.exists():
        return {
            "date": date,
            "screenshots": [],
            "count": 0
        }
    
    screenshots = []
    for img_file in screenshot_dir.glob("*.png"):
        screenshots.append({
            "filename": img_file.name,
            "timestamp": img_file.stem,  # Assuming filename is timestamp
            "path": str(img_file.relative_to(STORAGE_PATH))
        })
    
    screenshots.sort(key=lambda x: x['filename'])
    
    return {
        "date": date,
        "screenshots": screenshots,
        "count": len(screenshots)
    }

@app.get("/screenshots/{date}/{filename}")
def get_screenshot(date: str, filename: str):
    """Serve a specific screenshot file"""
    screenshot_path = SCREENSHOTS_PATH / date / filename
    
    if not screenshot_path.exists():
        raise HTTPException(status_code=404, detail="Screenshot not found")
    
    return FileResponse(screenshot_path)

@app.get("/analytics/summary")
def get_analytics_summary(days: int = 30):
    """Get analytics summary for the last N days"""
    end_date = datetime.now()
    total_work_hours = 0
    total_active_minutes = 0
    total_idle_minutes = 0
    days_worked = 0
    
    for i in range(days):
        date = end_date - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        activities = load_activity_log(date_str)
        
        if activities:
            stats = calculate_daily_stats(activities)
            total_work_hours += stats['total_work_hours']
            total_active_minutes += stats['total_active_minutes']
            total_idle_minutes += stats['total_idle_minutes']
            days_worked += 1
    
    avg_work_hours = total_work_hours / days_worked if days_worked > 0 else 0
    
    return {
        "period": f"Last {days} days",
        "total_work_hours": round(total_work_hours, 2),
        "total_active_minutes": round(total_active_minutes, 2),
        "total_idle_minutes": round(total_idle_minutes, 2),
        "days_worked": days_worked,
        "average_work_hours_per_day": round(avg_work_hours, 2),
        "employee": load_device_info()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
