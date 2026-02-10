# 🚀 Workforce Tracking Dashboard

A **Hubstaff-like workforce tracking system** with a centralized dashboard. This is **Phase 1** of the project - a local dashboard that reads data from your existing desktop tracking agent.

## 📋 Project Overview

**Goal:** Build a comprehensive workforce tracking system starting from local data visualization, eventually evolving to centralized backend with AI/ML capabilities.

**Current Phase:** Phase 1 - Local Dashboard (No AI, No ERP, No Central DB)

### What You Have
✅ Desktop tracking agent (Python .exe)
✅ Local SQLite database (`local.db`)
✅ JSON activity logs (minute-by-minute tracking)
✅ Screenshot capture
✅ Employee device info

### What We Just Built
✅ FastAPI backend (reads JSON logs)
✅ React dashboard (beautiful UI)
✅ Real-time activity monitoring
✅ Timesheet with charts
✅ Detailed activity logs
✅ Screenshot viewer

## 🏗️ Architecture

```
Desktop Agent (Existing)
    ↓
SQLite + JSON Logs (Local Storage)
    ↓
FastAPI Backend (Read-Only)
    ↓
React Dashboard (Web UI)
```

**Key Principle:** The backend is **read-only**. It does NOT modify your agent's data.

## 📂 Project Structure

```
workforce-dashboard/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main application
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend docs
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API client
│   │   └── utils/            # Helper functions
│   ├── package.json          # Node dependencies
│   └── README.md             # Frontend docs
│
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 18+** (for frontend)
- **Desktop agent** with existing data

### Step 1: Configure Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **IMPORTANT:** Edit `main.py` and update the storage path:
```python
# Line 15-19 in main.py
STORAGE_PATH = Path("../agent/storage")  # ← UPDATE THIS PATH
```

Point it to your actual agent storage folder. For example:
- Windows: `Path("C:/Users/YourName/agent/storage")`
- Linux: `Path("/home/yourname/agent/storage")`
- Relative: `Path("../../your-agent/storage")`

4. Start the backend:
```bash
python main.py
```

Backend will run at `http://localhost:8000`

### Step 2: Start Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run at `http://localhost:3000`

### Step 3: Access Dashboard

Open your browser and go to: **http://localhost:3000**

You should see:
- Employee info in sidebar
- Today's activity stats
- Navigation to Timesheet, Activity, Screenshots

## 📊 Features

### 1. Today's Activity
- **Real-time stats** (auto-refreshes every 60 seconds)
- Total work hours
- Active vs idle time
- Productivity percentage
- Session count
- First login & last activity times
- Breaks and lunch tracking

### 2. Timesheet
- View **7, 14, or 30 days** of data
- **Bar charts** showing work hours trends
- Daily breakdown table
- Productivity scores
- Active vs total time comparison

### 3. Activity Log
- **Minute-by-minute** activity timeline
- Session detection (when agent restarts)
- Idle time tracking
- Break and lunch indicators
- Date selector

### 4. Screenshots
- **Gallery view** of captured screenshots
- Date-based filtering
- Full-screen preview
- Download capability
- Automatic error handling

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py`:

```python
# Storage paths
STORAGE_PATH = Path("YOUR_AGENT_PATH/storage")
ACTIVITY_LOGS_PATH = STORAGE_PATH / "activity_logs"
SCREENSHOTS_PATH = STORAGE_PATH / "screenshots"
DEVICE_INFO_PATH = STORAGE_PATH / "device.json"

# Server settings (in main.py at bottom)
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port if needed
```

### Frontend Configuration

Edit `frontend/vite.config.js` if backend port changes:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',  // Update if needed
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

## 📡 API Endpoints

The backend exposes these REST APIs:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/employee/info` | GET | Employee details |
| `/work/today` | GET | Today's statistics |
| `/work/timesheet?days=N` | GET | N-day timesheet |
| `/activity/detailed?date=YYYY-MM-DD` | GET | Activity log for date |
| `/screenshots/list?date=YYYY-MM-DD` | GET | List screenshots |
| `/screenshots/{date}/{filename}` | GET | Get screenshot file |
| `/analytics/summary?days=N` | GET | Analytics summary |

**API Documentation:** http://localhost:8000/docs (Swagger UI)

## 🎨 Screenshots

### Dashboard Preview
*(Run the app to see your actual data)*

**Today View:**
- Large stat cards showing work hours, active time, idle time
- Productivity gauge with color coding
- Work timeline with first/last activity

**Timesheet View:**
- Summary cards (total hours, days worked, average)
- Bar chart showing trends
- Detailed table with daily breakdowns

**Activity View:**
- Full activity log with timestamps
- Session restart detection
- Idle time highlighting

**Screenshots View:**
- Grid gallery of screenshots
- Click to view full-screen
- Download individual images

## 🔍 Troubleshooting

### Backend Issues

**"No such file or directory" error:**
- Check that `STORAGE_PATH` in `main.py` is correct
- Verify the agent storage folder exists
- Make sure you have read permissions

**"No activity found" in API:**
- Ensure activity log JSON files exist in `storage/activity_logs/`
- Check file naming: should be `YYYY-MM-DD.json`
- Verify agent has run and logged data

**API not starting:**
- Check if port 8000 is already in use
- Try changing port in `main.py`
- Ensure all dependencies are installed

### Frontend Issues

**Blank page or errors:**
- Check browser console for errors
- Ensure backend is running
- Verify API endpoint in `vite.config.js`

**No data showing:**
- Open Network tab in browser DevTools
- Check if API calls are successful
- Verify backend is returning data (test at http://localhost:8000/docs)

**CORS errors:**
- Backend has CORS middleware enabled by default
- If issues persist, check CORS configuration in `main.py`

### Data Issues

**Employee info not showing:**
- Verify `device.json` exists in storage folder
- Check JSON format is valid

**Screenshots not loading:**
- Ensure screenshots exist in `storage/screenshots/YYYY-MM-DD/`
- Verify file extensions are `.png`
- Check file permissions

## 🛣️ Roadmap

### ✅ Phase 1 - Local Dashboard (CURRENT)
- [x] Backend API (FastAPI)
- [x] React dashboard
- [x] Read-only data access
- [x] Real-time stats
- [x] Charts & visualizations
- [x] Screenshot viewer

### 🔄 Phase 2 - Central Backend (NEXT)
- [ ] PostgreSQL/MongoDB setup
- [ ] Multi-user support
- [ ] Admin dashboard
- [ ] Team analytics
- [ ] Data sync from agents
- [ ] Role-based access

### 🤖 Phase 3 - AI/ML Integration
- [ ] Productivity scoring
- [ ] App classification
- [ ] Anomaly detection
- [ ] Pattern recognition
- [ ] Predictive analytics

### 🧠 Phase 4 - LLM Features
- [ ] Natural language insights
- [ ] Chatbot assistant
- [ ] Report generation
- [ ] Recommendations
- [ ] Explain ML decisions

## 🤝 Contributing

This is currently a personal project, but suggestions are welcome!

## 📝 License

Private project - All rights reserved.

## 🙋 Support

For questions about:
- **Setup:** Check troubleshooting section above
- **API:** Visit http://localhost:8000/docs
- **Features:** See individual README files in backend/ and frontend/

## 🎯 Design Principles

1. **Truth First:** Show real data before adding AI/ML
2. **Read-Only:** Backend never modifies agent data
3. **Progressive Enhancement:** Start simple, add complexity gradually
4. **User-Centric:** Focus on what users need to see
5. **Privacy-Conscious:** All data stays local in Phase 1

## 📚 Tech Stack

**Backend:**
- FastAPI (Python web framework)
- Uvicorn (ASGI server)
- Python 3.8+

**Frontend:**
- React 18
- Vite (build tool)
- Tailwind CSS
- Recharts (charts)
- Lucide React (icons)
- Axios (HTTP client)

**Data:**
- SQLite (agent DB)
- JSON files (activity logs)
- Local filesystem (screenshots)

---

**Built with ❤️ for transparent workforce tracking**

Last Updated: February 2026
Version: 1.0.0 (Phase 1)
