# 🚀 Quick Start Guide

Get your Workforce Dashboard running in 5 minutes!

## Prerequisites

✅ Python 3.8 or higher
✅ Node.js 18 or higher
✅ Desktop agent with existing data

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
python setup.py
```

This will:
1. Find your agent storage folder automatically
2. Verify the folder structure
3. Show employee information
4. Configure the backend automatically

Then follow the on-screen instructions.

### Option 2: Manual Setup

#### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Edit main.py and update line 15:
# STORAGE_PATH = Path("/path/to/your/agent/storage")

# Start backend
python main.py
```

Backend will run at `http://localhost:8000`

#### Step 2: Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at `http://localhost:3000`

## Verification

1. **Backend API**: Visit http://localhost:8000/docs
   - You should see the Swagger API documentation

2. **Frontend Dashboard**: Visit http://localhost:3000
   - You should see the dashboard with your employee info

3. **Test Data**: Click on "Today" in the sidebar
   - If you have data for today, it will show
   - Otherwise, check "Timesheet" for historical data

## Troubleshooting

### Backend not starting?

**Check storage path:**
```bash
# In backend/main.py, verify line 15 points to your actual storage folder
# Example paths:
# Windows: Path("C:/Users/YourName/agent/storage")
# Linux: Path("/home/yourname/agent/storage")
```

**Verify folder structure:**
```
storage/
├── device.json          # Required
├── local.db            # Optional
├── activity_logs/      # Required
│   └── YYYY-MM-DD.json
└── screenshots/        # Optional
    └── YYYY-MM-DD/
```

**Test backend manually:**
```bash
# Visit in browser:
http://localhost:8000/employee/info

# Should return JSON with employee details
```

### Frontend not showing data?

**Check API connection:**
- Open browser DevTools (F12)
- Go to Network tab
- Refresh page
- Look for API calls to `/api/*`
- Check if they return 200 OK

**Common issues:**
- Backend not running → Start backend first
- Wrong API endpoint → Check `vite.config.js` proxy settings
- CORS errors → Backend has CORS enabled by default

### No data appearing?

**Verify data files exist:**
```bash
# Check if activity logs exist
ls agent/storage/activity_logs/

# Should show files like:
# 2026-01-22.json
# 2026-01-23.json
```

**Test with a specific date:**
- Go to "Activity" page
- Select a date where you know the agent was running
- Should show activity entries

## What to Expect

### If You Have Data

**Today Page:**
- Total work hours
- Active vs idle time
- Productivity percentage
- Session count

**Timesheet Page:**
- Bar charts showing trends
- Daily breakdown table
- Summary statistics

**Activity Page:**
- Minute-by-minute log
- Session detection
- Idle time tracking

**Screenshots Page:**
- Gallery of captured screenshots
- Full-screen preview
- Download option

### If You Don't Have Data

You'll see:
- Empty dashboards with helpful messages
- "No activity recorded" notices
- Instructions to start the desktop agent

**Next step:** Run your desktop agent to start collecting data!

## Daily Usage

1. **Start Backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Dashboard:**
   - Open http://localhost:3000
   - Dashboard auto-refreshes every 60 seconds

## Production Deployment (Later)

For now, run in development mode. Production deployment will come in Phase 2.

## Need Help?

1. Check the main [README.md](./README.md)
2. Review [Backend README](./backend/README.md)
3. Review [Frontend README](./frontend/README.md)
4. Check API docs at http://localhost:8000/docs

## Next Steps

Once running successfully:

✅ Explore all dashboard pages
✅ Check timesheet for historical data
✅ View activity logs
✅ Browse screenshots
✅ Familiarize yourself with the data structure

Then prepare for **Phase 2: Central Backend** when ready!

---

**Happy tracking! 📊**
