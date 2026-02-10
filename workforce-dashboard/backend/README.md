# Workforce Dashboard - Backend

FastAPI backend for the workforce tracking dashboard. Reads activity logs from the desktop agent.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure paths:**
Edit `main.py` and update these paths to match your agent's storage location:
```python
STORAGE_PATH = Path("../agent/storage")  # Update this
```

3. **Run the server:**
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### Employee
- `GET /employee/info` - Get employee device information

### Work Stats
- `GET /work/today` - Today's work statistics
- `GET /work/timesheet?days=7` - Timesheet for last N days (default 7)

### Activity
- `GET /activity/detailed?date=YYYY-MM-DD` - Detailed activity log for a date

### Screenshots
- `GET /screenshots/list?date=YYYY-MM-DD` - List screenshots for a date
- `GET /screenshots/{date}/{filename}` - Get a specific screenshot

### Analytics
- `GET /analytics/summary?days=30` - Summary analytics for last N days

## Example Responses

### GET /work/today
```json
{
  "date": "2026-01-22",
  "stats": {
    "total_work_hours": 2.15,
    "total_active_minutes": 118.5,
    "total_idle_minutes": 10.5,
    "sessions": 3,
    "first_login": "12:14",
    "last_activity": "17:51",
    "breaks_taken": 2,
    "lunch_taken": false
  },
  "employee": {
    "employee_id": "SLTPL-FY20-0054",
    "employee_name": "Saurabh Jasoriya",
    ...
  }
}
```

## Project Structure
```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Notes

- Backend is **read-only** - it does not modify any agent data
- Uses existing JSON log files from the desktop agent
- No database required for Phase 1
- CORS enabled for local development
