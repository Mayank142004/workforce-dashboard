export const formatTime = (hours) => {
  const totalMinutes = Math.floor(hours * 60);
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return `${h}h ${m}m`;
};

export const formatMinutes = (minutes) => {
  const h = Math.floor(minutes / 60);
  const m = Math.floor(minutes % 60);
  if (h > 0) {
    return `${h}h ${m}m`;
  }
  return `${m}m`;
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    weekday: 'short', 
    month: 'short', 
    day: 'numeric' 
  });
};

export const formatDateLong = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric',
    month: 'long', 
    day: 'numeric' 
  });
};

export const getProductivityPercentage = (activeMinutes, totalMinutes) => {
  if (totalMinutes === 0) return 0;
  return Math.round((activeMinutes / totalMinutes) * 100);
};

export const getStatusColor = (percentage) => {
  if (percentage >= 80) return 'text-green-600 bg-green-50';
  if (percentage >= 60) return 'text-yellow-600 bg-yellow-50';
  return 'text-red-600 bg-red-50';
};
