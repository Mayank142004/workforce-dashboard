# Workforce Dashboard - Frontend

Modern React dashboard for the workforce tracking system.

## Features

✅ **Today's Activity** - Real-time work statistics for the current day
✅ **Timesheet** - View work hours over 7, 14, or 30 days with charts
✅ **Activity Log** - Detailed minute-by-minute activity timeline
✅ **Screenshots** - Browse captured screenshots by date
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Auto-refresh** - Today page refreshes automatically every 60 seconds

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **Axios** - API requests
- **React Router** - Navigation

## Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Configure API endpoint:**
The frontend is configured to proxy API requests to `http://localhost:8000` via Vite.
If your backend runs on a different port, edit `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:YOUR_PORT',
      ...
    }
  }
}
```

3. **Run development server:**
```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

4. **Build for production:**
```bash
npm run build
```

Built files will be in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.jsx         # Main layout with sidebar
│   │   └── StatCard.jsx       # Reusable stat card component
│   ├── pages/
│   │   ├── Today.jsx          # Today's activity page
│   │   ├── Timesheet.jsx      # Timesheet with charts
│   │   ├── Activity.jsx       # Detailed activity log
│   │   └── Screenshots.jsx    # Screenshot gallery
│   ├── services/
│   │   └── api.js             # API client
│   ├── utils/
│   │   └── helpers.js         # Utility functions
│   ├── App.jsx                # Main app component
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## API Integration

The frontend communicates with the FastAPI backend through these endpoints:

- `GET /employee/info` - Employee information
- `GET /work/today` - Today's statistics
- `GET /work/timesheet?days=N` - Timesheet data
- `GET /activity/detailed?date=YYYY-MM-DD` - Activity log
- `GET /screenshots/list?date=YYYY-MM-DD` - Screenshot list
- `GET /screenshots/{date}/{filename}` - Screenshot file

## Customization

### Colors
Edit `tailwind.config.js` to customize the color scheme:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      },
    },
  },
}
```

### Auto-refresh Interval
Edit `Today.jsx` to change the refresh interval (default: 60 seconds):

```javascript
const interval = setInterval(loadTodayStats, 60000); // milliseconds
```

## Screenshots

### Today's Activity
- Real-time work stats
- Productivity gauge
- Work timeline

### Timesheet
- 7/14/30 day views
- Bar charts
- Detailed daily breakdown

### Activity Log
- Minute-by-minute tracking
- Session detection
- Idle time highlighting

### Screenshots
- Date-based gallery
- Full-screen preview
- Download capability

## Development Tips

1. **Hot Reload**: Changes are reflected immediately during development
2. **API Errors**: Check browser console for detailed error messages
3. **CORS**: If you encounter CORS issues, ensure the backend has CORS middleware enabled
4. **Date Format**: All dates use `YYYY-MM-DD` format for consistency

## Troubleshooting

**Backend not responding:**
- Ensure backend is running on port 8000
- Check backend logs for errors

**No data showing:**
- Verify the backend can access the agent's storage folder
- Check that JSON log files exist in `storage/activity_logs/`

**Screenshots not loading:**
- Verify screenshot files exist in `storage/screenshots/YYYY-MM-DD/`
- Check file permissions

## Future Enhancements

- [ ] User authentication
- [ ] Admin dashboard
- [ ] Team analytics
- [ ] Export reports (PDF/Excel)
- [ ] Email notifications
- [ ] Mobile app
