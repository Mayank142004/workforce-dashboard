import React, { useState, useEffect } from 'react';
import { Activity as ActivityIcon, Calendar } from 'lucide-react';
import { workforceAPI } from '../services/api';
import { formatDateLong } from '../utils/helpers';

const Activity = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split('T')[0]
  );

  useEffect(() => {
    loadActivity();
  }, [selectedDate]);

  const loadActivity = async () => {
    try {
      setLoading(true);
      const response = await workforceAPI.getDetailedActivity(selectedDate);
      setData(response.data);
    } catch (err) {
      console.error('Error loading activity:', err);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading activity...</p>
        </div>
      </div>
    );
  }

  const activities = data?.activities || [];
  const stats = data?.stats || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Activity Log</h1>
          <p className="text-gray-600 mt-1">Detailed activity timeline</p>
        </div>
        <div className="flex items-center space-x-2">
          <Calendar className="w-5 h-5 text-gray-500" />
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Stats Summary */}
      {activities.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="stat-card">
            <p className="text-sm font-medium text-gray-600">Total Entries</p>
            <p className="text-2xl font-bold text-gray-900">{data.total_entries}</p>
          </div>
          <div className="stat-card">
            <p className="text-sm font-medium text-gray-600">Work Hours</p>
            <p className="text-2xl font-bold text-gray-900">
              {stats.total_work_hours?.toFixed(2) || 0}h
            </p>
          </div>
          <div className="stat-card">
            <p className="text-sm font-medium text-gray-600">Sessions</p>
            <p className="text-2xl font-bold text-gray-900">{stats.sessions || 0}</p>
          </div>
          <div className="stat-card">
            <p className="text-sm font-medium text-gray-600">Breaks</p>
            <p className="text-2xl font-bold text-gray-900">{stats.breaks_taken || 0}</p>
          </div>
        </div>
      )}

      {/* Activity Timeline */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Timeline for {formatDateLong(selectedDate)}
        </h3>
        
        {activities.length === 0 ? (
          <div className="text-center py-12">
            <ActivityIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No activity recorded for this date</p>
            <p className="text-sm text-gray-500 mt-2">
              Select a different date or start the desktop agent
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Cumulative Hours
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Idle Seconds
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Breaks
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Lunch
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {activities.map((activity, index) => {
                  const time = new Date(activity.timestamp).toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                  });
                  
                  // Detect session restart
                  const isSessionStart = index > 0 && 
                    activity.normal_hours < activities[index - 1].normal_hours;
                  
                  return (
                    <tr 
                      key={index} 
                      className={`hover:bg-gray-50 ${isSessionStart ? 'border-t-2 border-primary-500' : ''}`}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <span className="text-sm font-medium text-gray-900">{time}</span>
                          {isSessionStart && (
                            <span className="ml-2 px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded">
                              New Session
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {activity.normal_hours.toFixed(2)}h
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`text-sm ${
                          activity.idle_seconds > 60 ? 'text-yellow-600 font-medium' : 'text-gray-900'
                        }`}>
                          {activity.idle_seconds}s
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {activity.breaks_used}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          activity.lunch_used 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {activity.lunch_used ? 'Yes' : 'No'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>Activity Log:</strong> Shows minute-by-minute tracking data. 
          "New Session" markers indicate when the agent was restarted. 
          Idle seconds show periods of inactivity detected by the agent.
        </p>
      </div>
    </div>
  );
};

export default Activity;
