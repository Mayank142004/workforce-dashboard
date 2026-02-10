import React, { useState, useEffect } from 'react';
import { Clock, Activity, Coffee, PlayCircle, StopCircle, TrendingUp } from 'lucide-react';
import StatCard from '../components/StatCard';
import { workforceAPI } from '../services/api';
import { formatTime, formatMinutes, getProductivityPercentage } from '../utils/helpers';

const Today = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTodayStats();
    // Refresh every 60 seconds
    const interval = setInterval(loadTodayStats, 60000);
    return () => clearInterval(interval);
  }, []);

  const loadTodayStats = async () => {
    try {
      setLoading(true);
      const response = await workforceAPI.getTodayStats();
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load today\'s statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading today's stats...</p>
        </div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-600">{error}</p>
        <button 
          onClick={loadTodayStats}
          className="mt-4 btn-primary"
        >
          Retry
        </button>
      </div>
    );
  }

  const stats = data?.stats || {};
  const totalMinutes = stats.total_work_hours * 60;
  const productivityPercent = getProductivityPercentage(stats.total_active_minutes, totalMinutes);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Today's Activity</h1>
          <p className="text-gray-600 mt-1">
            {new Date().toLocaleDateString('en-US', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </p>
        </div>
        <button 
          onClick={loadTodayStats}
          className="btn-secondary flex items-center space-x-2"
          disabled={loading}
        >
          <Activity className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Work Time"
          value={formatTime(stats.total_work_hours || 0)}
          subtitle={`${stats.sessions || 0} session${stats.sessions !== 1 ? 's' : ''}`}
          icon={Clock}
          color="primary"
        />
        
        <StatCard
          title="Active Time"
          value={formatMinutes(stats.total_active_minutes || 0)}
          subtitle={`${productivityPercent}% productive`}
          icon={Activity}
          color="green"
        />
        
        <StatCard
          title="Idle Time"
          value={formatMinutes(stats.total_idle_minutes || 0)}
          subtitle="Time away from desk"
          icon={Coffee}
          color="yellow"
        />
        
        <StatCard
          title="Breaks Taken"
          value={stats.breaks_taken || 0}
          subtitle={stats.lunch_taken ? 'Lunch included' : 'No lunch yet'}
          icon={Coffee}
          color="blue"
        />
      </div>

      {/* Timeline */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Work Timeline</h3>
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center justify-center w-10 h-10 bg-green-50 rounded-full">
              <PlayCircle className="w-5 h-5 text-green-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">First Login</p>
              <p className="text-sm text-gray-600">{stats.first_login || 'Not started'}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center justify-center w-10 h-10 bg-blue-50 rounded-full">
              <StopCircle className="w-5 h-5 text-blue-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Last Activity</p>
              <p className="text-sm text-gray-600">{stats.last_activity || 'Not started'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Productivity Gauge */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Productivity Score</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-3xl font-bold text-gray-900">{productivityPercent}%</span>
            <TrendingUp className={`w-8 h-8 ${
              productivityPercent >= 80 ? 'text-green-600' : 
              productivityPercent >= 60 ? 'text-yellow-600' : 
              'text-red-600'
            }`} />
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div 
              className={`h-4 rounded-full transition-all ${
                productivityPercent >= 80 ? 'bg-green-600' : 
                productivityPercent >= 60 ? 'bg-yellow-600' : 
                'bg-red-600'
              }`}
              style={{ width: `${productivityPercent}%` }}
            />
          </div>
          <p className="text-sm text-gray-600">
            Based on active vs idle time ratio. Active time includes keyboard/mouse activity.
          </p>
        </div>
      </div>

      {stats.total_work_hours === 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <p className="text-blue-900 font-medium">No activity recorded yet today</p>
          <p className="text-blue-700 mt-2">
            Start the desktop agent to begin tracking your work time.
          </p>
        </div>
      )}
    </div>
  );
};

export default Today;
