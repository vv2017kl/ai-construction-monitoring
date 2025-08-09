import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Calendar, Clock, Play, Pause, SkipBack, SkipForward,
  Volume2, VolumeX, Download, Share2, Bookmark, Search,
  Filter, ChevronLeft, ChevronRight, Maximize2, Settings,
  AlertTriangle, Camera, MapPin, Eye, FileText, Image,
  FastForward, Rewind, RotateCcw, ZoomIn, ZoomOut
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockCameras, mockSites, mockUser, mockAlerts } from '../../data/mockData';

const VideoReview = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const videoRef = useRef(null);

  // State management
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedCamera, setSelectedCamera] = useState(mockCameras[0].id);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(86400); // 24 hours in seconds
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [volume, setVolume] = useState(0.7);
  const [isMuted, setIsMuted] = useState(false);
  const [showTimeline, setShowTimeline] = useState(true);
  const [bookmarks, setBookmarks] = useState([
    { time: 8400, label: 'Morning Safety Check', type: 'safety' },
    { time: 32400, label: 'Equipment Arrival', type: 'activity' },
    { time: 45000, label: 'PPE Violation Alert', type: 'alert' },
    { time: 61200, label: 'End of Shift', type: 'activity' }
  ]);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];
  const selectedCameraObj = mockCameras.find(c => c.id === selectedCamera);

  // Generate activity data for timeline visualization
  const generateActivityData = () => {
    const activities = [];
    for (let hour = 0; hour < 24; hour++) {
      const baseActivity = hour >= 6 && hour <= 18 ? Math.random() * 100 : Math.random() * 20;
      activities.push({
        hour,
        activity: Math.max(5, baseActivity),
        incidents: hour >= 8 && hour <= 17 ? Math.floor(Math.random() * 3) : 0
      });
    }
    return activities;
  };

  const [activityData] = useState(generateActivityData());

  // Time formatting utilities
  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // Playback controls
  const togglePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const changePlaybackSpeed = (speed) => {
    setPlaybackSpeed(speed);
  };

  const seekToTime = (time) => {
    setCurrentTime(time);
  };

  const addBookmark = () => {
    const newBookmark = {
      time: currentTime,
      label: `Bookmark ${bookmarks.length + 1}`,
      type: 'custom'
    };
    setBookmarks([...bookmarks, newBookmark].sort((a, b) => a.time - b.time));
  };

  const jumpToBookmark = (time) => {
    setCurrentTime(time);
  };

  // Video player component
  const VideoPlayer = () => (
    <div className="relative bg-gray-900 rounded-lg overflow-hidden" style={{ aspectRatio: '16/9' }}>
      {/* Simulated Video Content */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-300 via-gray-400 to-amber-200">
        {/* Construction site simulation */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-white">
            {/* Timestamp overlay */}
            <div className="absolute top-4 left-4 bg-black/70 px-3 py-1 rounded text-sm">
              {new Date(new Date(selectedDate).getTime() + currentTime * 1000).toLocaleString()}
            </div>
            
            {/* Camera info */}
            <div className="absolute top-4 right-4 bg-black/70 px-3 py-1 rounded text-sm">
              📹 {selectedCameraObj?.name}
            </div>

            {/* Playback speed indicator */}
            {playbackSpeed !== 1 && (
              <div className="absolute top-14 right-4 bg-blue-600 px-2 py-1 rounded text-xs">
                {playbackSpeed}x
              </div>
            )}

            {/* Simulated construction activity */}
            <div className="w-64 h-32 bg-yellow-400/30 rounded-lg flex items-center justify-center">
              <Camera className="w-16 h-16 text-white/50" />
            </div>
          </div>
        </div>

        {/* Play/Pause overlay */}
        {!isPlaying && (
          <div 
            className="absolute inset-0 flex items-center justify-center cursor-pointer"
            onClick={togglePlayPause}
          >
            <div className="bg-black/50 p-4 rounded-full">
              <Play className="w-12 h-12 text-white" />
            </div>
          </div>
        )}
      </div>

      {/* Video controls overlay */}
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
        <div className="flex items-center space-x-4">
          <button
            onClick={togglePlayPause}
            className="p-2 text-white hover:bg-white/20 rounded transition-colors"
          >
            {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
          </button>

          <div className="flex-1 flex items-center space-x-2">
            <span className="text-white text-sm">{formatTime(currentTime)}</span>
            <div className="flex-1 relative">
              <input
                type="range"
                min="0"
                max={duration}
                value={currentTime}
                onChange={(e) => seekToTime(parseInt(e.target.value))}
                className="w-full h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, ${theme.primary[500]} 0%, ${theme.primary[500]} ${(currentTime/duration)*100}%, #4b5563 ${(currentTime/duration)*100}%, #4b5563 100%)`
                }}
              />
              
              {/* Timeline markers for bookmarks */}
              {bookmarks.map((bookmark, index) => (
                <div
                  key={index}
                  className="absolute top-0 w-2 h-1 bg-yellow-400 rounded cursor-pointer"
                  style={{ left: `${(bookmark.time / duration) * 100}%` }}
                  onClick={() => jumpToBookmark(bookmark.time)}
                  title={bookmark.label}
                />
              ))}
            </div>
            <span className="text-white text-sm">{formatTime(duration)}</span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsMuted(!isMuted)}
              className="p-2 text-white hover:bg-white/20 rounded transition-colors"
            >
              {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
            </button>

            <button className="p-2 text-white hover:bg-white/20 rounded transition-colors">
              <Maximize2 className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  // Timeline visualization component
  const TimelineVisualization = () => (
    <div className="bg-white rounded-lg p-4 border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-900">Activity Timeline - {formatDate(selectedDate)}</h3>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowTimeline(!showTimeline)}
            className="text-sm text-blue-600 hover:text-blue-700"
          >
            {showTimeline ? 'Hide' : 'Show'} Timeline
          </button>
        </div>
      </div>

      {showTimeline && (
        <div className="space-y-4">
          {/* Hour-by-hour activity bars */}
          <div className="grid grid-cols-24 gap-1">
            {activityData.map((data, index) => (
              <div
                key={index}
                className="relative cursor-pointer group"
                onClick={() => seekToTime(data.hour * 3600)}
              >
                <div
                  className={`w-full rounded-sm transition-colors ${
                    Math.floor(currentTime / 3600) === data.hour 
                      ? 'bg-blue-600' 
                      : data.incidents > 0 
                      ? 'bg-red-400' 
                      : 'bg-gray-300'
                  }`}
                  style={{ height: `${Math.max(4, data.activity / 2)}px` }}
                />
                <div className="absolute -bottom-5 left-0 text-xs text-gray-500 transform -rotate-45 origin-left">
                  {data.hour}
                </div>
                
                {/* Tooltip */}
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-black text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                  {data.hour}:00 - Activity: {Math.round(data.activity)}%
                  {data.incidents > 0 && `, ${data.incidents} incidents`}
                </div>
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className="flex items-center space-x-4 text-xs">
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-gray-300 rounded"></div>
              <span>Normal Activity</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-red-400 rounded"></div>
              <span>Incidents</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-blue-600 rounded"></div>
              <span>Current Time</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Historical Video Review</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Calendar className="w-3 h-3" />
                <span>{formatDate(selectedDate)}</span>
                <span>•</span>
                <Camera className="w-3 h-3" />
                <span>{selectedCameraObj?.name}</span>
                <span>•</span>
                <span>{formatTime(currentTime)}</span>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[0.5, 1, 2, 4, 8].map((speed) => (
                  <button
                    key={speed}
                    onClick={() => changePlaybackSpeed(speed)}
                    className={`px-3 py-1 text-sm rounded transition-colors ${
                      playbackSpeed === speed 
                        ? 'bg-white shadow-sm text-blue-600' 
                        : 'hover:bg-gray-200'
                    }`}
                  >
                    {speed}x
                  </button>
                ))}
              </div>

              <button
                onClick={addBookmark}
                className="flex items-center space-x-2 px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors"
              >
                <Bookmark className="w-4 h-4" />
                <span>Bookmark</span>
              </button>

              <button className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Video Area */}
          <div className="flex-1 p-6 space-y-6">
            <VideoPlayer />
            <TimelineVisualization />
          </div>

          {/* Right Panel */}
          <div className="w-80 bg-gray-50 border-l border-gray-200 p-6 space-y-6 overflow-y-auto">
            {/* Date & Camera Selection */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-4">Video Selection</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Date</label>
                  <input
                    type="date"
                    value={selectedDate}
                    onChange={(e) => setSelectedDate(e.target.value)}
                    max={new Date().toISOString().split('T')[0]}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:border-transparent"
                    style={{ '--tw-ring-color': theme.primary[500] + '40' }}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Camera</label>
                  <select
                    value={selectedCamera}
                    onChange={(e) => setSelectedCamera(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:border-transparent"
                    style={{ '--tw-ring-color': theme.primary[500] + '40' }}
                  >
                    {mockCameras.map((camera) => (
                      <option key={camera.id} value={camera.id}>
                        {camera.name} - {camera.location}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Bookmarks */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-4">Bookmarks ({bookmarks.length})</h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {bookmarks.map((bookmark, index) => (
                  <div
                    key={index}
                    className="p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                    onClick={() => jumpToBookmark(bookmark.time)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${
                          bookmark.type === 'alert' ? 'bg-red-500' :
                          bookmark.type === 'safety' ? 'bg-yellow-500' :
                          bookmark.type === 'activity' ? 'bg-blue-500' : 'bg-gray-500'
                        }`}></div>
                        <span className="text-sm font-medium text-gray-900">{bookmark.label}</span>
                      </div>
                      <span className="text-xs text-gray-500">{formatTime(bookmark.time)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Quick Actions</h3>
              <div className="space-y-2">
                <button
                  onClick={() => navigate('/time-comparison')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <Clock className="w-5 h-5 text-blue-600" />
                  <div>
                    <div className="font-medium text-blue-900">Compare Times</div>
                    <div className="text-xs text-blue-600">Side-by-side analysis</div>
                  </div>
                </button>
                
                <button
                  onClick={() => navigate('/time-lapse')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                >
                  <FastForward className="w-5 h-5 text-green-600" />
                  <div>
                    <div className="font-medium text-green-900">Time Lapse</div>
                    <div className="text-xs text-green-600">Compressed timeline view</div>
                  </div>
                </button>

                <button
                  onClick={() => navigate('/alert-center')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                >
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                  <div>
                    <div className="font-medium text-red-900">View Alerts</div>
                    <div className="text-xs text-red-600">See incidents for this time</div>
                  </div>
                </button>
              </div>
            </div>

            {/* Export Options */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Export Options</h3>
              <div className="space-y-2">
                <button className="w-full flex items-center space-x-3 p-2 text-left hover:bg-gray-50 rounded-lg transition-colors">
                  <Image className="w-4 h-4 text-gray-600" />
                  <span className="text-sm">Screenshot</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-2 text-left hover:bg-gray-50 rounded-lg transition-colors">
                  <FileText className="w-4 h-4 text-gray-600" />
                  <span className="text-sm">Video Clip</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-2 text-left hover:bg-gray-50 rounded-lg transition-colors">
                  <Share2 className="w-4 h-4 text-gray-600" />
                  <span className="text-sm">Share Link</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default VideoReview;