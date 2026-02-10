import React, { useState, useEffect } from 'react';
import { Calendar, TrendingUp, TrendingDown } from 'lucide-react';
import { workforceAPI } from '../services/api';
import { formatTime, formatMinutes, getProductivityPercentage, formatDate } from '../utils/helpers';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const Timesheet = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [period, setPeriod] = useState(7);

  useEffect(() => {
    loadTimesheet();
  }, [period]);

  const loadTimesheet = async () => {
    try {
      setLoading(true);
      const response = await workforceAPI.getTimesheet(period);
      setData(response.data);
    } catch (err) {
      console.error('Error loading timesheet:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading timesheet...</p>
        </div>
      </div>
    );
  }

  const timesheet = data?.timesheet || [];
  
  // Calculate totals
  const totalHours = timesheet.reduce((sum, day) => sum + (day.stats.total_work_hours || 0), 0);
  const totalActiveMinutes = timesheet.reduce((sum, day) => sum + (day.stats.total_active_minutes || 0), 0);
  const daysWorked = timesheet.filter(day => day.stats.total_work_hours > 0).length;
  const avgHoursPerDay = daysWorked > 0 ? totalHours / daysWorked : 0;

  // Prepare chart data
  const chartData = [...timesheet].reverse().map(day => ({
    date: formatDate(day.date),
    hours: parseFloat((day.stats.total_work_hours || 0).toFixed(2)),
    active: parseFloat((day.stats.total_active_minutes / 60 || 0).toFixed(2)),
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Timesheet</h1>
          <p className="text-gray-600 mt-1">Your work hours and activity log</p>
        </div>
        <div className="flex space-x-2">
          {[7, 14, 30].map(days => (
            <button
              key={days}
              onClick={() => setPeriod(days)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                period === days 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {days} days
            </button>
          ))}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="stat-card">
          <p className="text-sm font-medium text-gray-600 mb-1">Total Hours</p>
          <p className="text-3xl font-bold text-gray-900">{formatTime(totalHours)}</p>
          <p className="text-sm text-gray-500 mt-1">{period} days</p>
        </div>
        
        <div className="stat-card">
          <p className="text-sm font-medium text-gray-600 mb-1">Days Worked</p>
          <p className="text-3xl font-bold text-gray-900">{daysWorked}</p>
          <p className="text-sm text-gray-500 mt-1">out of {period}</p>
        </div>
        
        <div className="stat-card">
          <p className="text-sm font-medium text-gray-600 mb-1">Avg Hours/Day</p>
          <p className="text-3xl font-bold text-gray-900">{formatTime(avgHoursPerDay)}</p>
          <p className="text-sm text-gray-500 mt-1">when working</p>
        </div>
        
        <div className="stat-card">
          <p className="text-sm font-medium text-gray-600 mb-1">Active Time</p>
          <p className="text-3xl font-bold text-gray-900">{formatMinutes(totalActiveMinutes)}</p>
          <p className="text-sm text-gray-500 mt-1">
            {getProductivityPercentage(totalActiveMinutes, totalHours * 60)}% productive
          </p>
        </div>
      </div>

      {/* Chart */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Work Hours Trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis label={{ value: 'Hours', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="hours" fill="#0ea5e9" name="Total Hours" />
            <Bar dataKey="active" fill="#10b981" name="Active Hours" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Table */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Daily Breakdown</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Work Hours
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Active Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Idle Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sessions
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Productivity
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {timesheet.map((day) => {
                const stats = day.stats;
                const productivity = getProductivityPercentage(
                  stats.total_active_minutes, 
                  stats.total_work_hours * 60
                );
                
                return (
                  <tr key={day.date} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{day.day}</div>
                        <div className="text-sm text-gray-500">{formatDate(day.date)}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 font-medium">
                        {formatTime(stats.total_work_hours || 0)}
                      </div>
                      {stats.first_login && (
                        <div className="text-xs text-gray-500">
                          {stats.first_login} - {stats.last_activity}
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatMinutes(stats.total_active_minutes || 0)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatMinutes(stats.total_idle_minutes || 0)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stats.sessions || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className={`text-sm font-medium ${
                          productivity >= 80 ? 'text-green-600' : 
                          productivity >= 60 ? 'text-yellow-600' : 
                          'text-red-600'
                        }`}>
                          {productivity}%
                        </span>
                        {productivity >= 80 ? (
                          <TrendingUp className="w-4 h-4 ml-2 text-green-600" />
                        ) : productivity < 60 ? (
                          <TrendingDown className="w-4 h-4 ml-2 text-red-600" />
                        ) : null}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Timesheet;
