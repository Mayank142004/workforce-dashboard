import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const workforceAPI = {
  // Employee
  getEmployeeInfo: () => api.get('/employee/info'),
  
  // Work Stats
  getTodayStats: () => api.get('/work/today'),
  getTimesheet: (days = 7) => api.get(`/work/timesheet?days=${days}`),
  
  // Activity
  getDetailedActivity: (date = null) => {
    const url = date ? `/activity/detailed?date=${date}` : '/activity/detailed';
    return api.get(url);
  },
  
  // Screenshots
  listScreenshots: (date = null) => {
    const url = date ? `/screenshots/list?date=${date}` : '/screenshots/list';
    return api.get(url);
  },
  getScreenshotUrl: (date, filename) => `${API_BASE_URL}/screenshots/${date}/${filename}`,
  
  // Analytics
  getAnalyticsSummary: (days = 30) => api.get(`/analytics/summary?days=${days}`),
};

export default api;
