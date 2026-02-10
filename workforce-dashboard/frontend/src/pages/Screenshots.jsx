import React, { useState, useEffect } from 'react';
import { Image, Calendar, Download } from 'lucide-react';
import { workforceAPI } from '../services/api';
import { formatDateLong } from '../utils/helpers';

const Screenshots = () => {
  const [loading, setLoading] = useState(true);
  const [screenshots, setScreenshots] = useState([]);
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    loadScreenshots();
  }, [selectedDate]);

  const loadScreenshots = async () => {
    try {
      setLoading(true);
      const response = await workforceAPI.listScreenshots(selectedDate);
      setScreenshots(response.data.screenshots || []);
    } catch (err) {
      console.error('Error loading screenshots:', err);
      setScreenshots([]);
    } finally {
      setLoading(false);
    }
  };

  const openImageModal = (screenshot) => {
    setSelectedImage(screenshot);
  };

  const closeModal = () => {
    setSelectedImage(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading screenshots...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Screenshots</h1>
          <p className="text-gray-600 mt-1">Activity screenshots captured by the agent</p>
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

      {/* Screenshots Grid */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            {formatDateLong(selectedDate)}
          </h3>
          <span className="text-sm text-gray-600">
            {screenshots.length} screenshot{screenshots.length !== 1 ? 's' : ''}
          </span>
        </div>

        {screenshots.length === 0 ? (
          <div className="text-center py-12">
            <Image className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No screenshots available for this date</p>
            <p className="text-sm text-gray-500 mt-2">
              Screenshots are captured periodically by the desktop agent
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {screenshots.map((screenshot, index) => (
              <div
                key={index}
                className="group relative bg-gray-100 rounded-lg overflow-hidden cursor-pointer hover:ring-2 hover:ring-primary-500 transition-all"
                onClick={() => openImageModal(screenshot)}
              >
                <div className="aspect-video relative">
                  <img
                    src={workforceAPI.getScreenshotUrl(selectedDate, screenshot.filename)}
                    alt={`Screenshot ${screenshot.timestamp}`}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23f3f4f6" width="100" height="100"/%3E%3Ctext fill="%239ca3af" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle"%3EImage Error%3C/text%3E%3C/svg%3E';
                    }}
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all flex items-center justify-center">
                    <Download className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                </div>
                <div className="p-3 bg-white">
                  <p className="text-xs font-medium text-gray-900 truncate">
                    {screenshot.filename}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {screenshot.timestamp}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4"
          onClick={closeModal}
        >
          <div
            className="relative max-w-6xl max-h-full"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={closeModal}
              className="absolute -top-10 right-0 text-white hover:text-gray-300 text-2xl font-bold"
            >
              ✕
            </button>
            <img
              src={workforceAPI.getScreenshotUrl(selectedDate, selectedImage.filename)}
              alt={`Screenshot ${selectedImage.timestamp}`}
              className="max-w-full max-h-[90vh] rounded-lg"
            />
            <div className="mt-4 bg-white rounded-lg p-4">
              <p className="font-medium text-gray-900">{selectedImage.filename}</p>
              <p className="text-sm text-gray-600 mt-1">Timestamp: {selectedImage.timestamp}</p>
              <a
                href={workforceAPI.getScreenshotUrl(selectedDate, selectedImage.filename)}
                download={selectedImage.filename}
                className="mt-3 inline-flex items-center space-x-2 btn-primary"
              >
                <Download className="w-4 h-4" />
                <span>Download</span>
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>Privacy Note:</strong> Screenshots are captured locally by the desktop agent 
          and stored on your device. They are only accessible through this dashboard when 
          connected to your local machine.
        </p>
      </div>
    </div>
  );
};

export default Screenshots;
