import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Shield, Camera, MapPin, AlertTriangle, Building2 } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: 'j.wilson@skylineconstruction.com',
    password: 'demo123',
    rememberDevice: true,
    selectedPortal: 'solution-user' // Default portal
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { theme } = useTheme();

  const portals = [
    {
      id: 'solution-user',
      name: 'Construction Portal',
      description: 'Site Managers, Safety Officers, Project Coordinators',
      icon: <Shield className="w-6 h-6" />,
      route: '/dashboard'
    },
    {
      id: 'solution-admin',
      name: 'Admin Portal',
      description: 'Company Executives, System Administrators',
      icon: <Building2 className="w-6 h-6" />,
      route: '/admin/dashboard'
    },
    {
      id: 'vms-user',
      name: 'VMS Operations',
      description: 'Security Personnel, Camera Operators',
      icon: <Camera className="w-6 h-6" />,
      route: '/vms/operations'
    },
    {
      id: 'vms-admin',
      name: 'VMS Admin',
      description: 'IT Staff, VMS System Administrators',
      icon: <AlertTriangle className="w-6 h-6" />,
      route: '/vms/admin'
    }
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate authentication
    setTimeout(() => {
      const selectedPortal = portals.find(p => p.id === formData.selectedPortal);
      navigate(selectedPortal.route);
      setIsLoading(false);
    }, 1000);
  };

  const selectedPortalData = portals.find(p => p.id === formData.selectedPortal);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-blue-50 to-slate-200 flex items-center justify-center p-4">
      {/* Background Pattern */}
      <div 
        className="absolute inset-0 opacity-10" 
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23${theme.primary[500].replace('#', '')}' fill-opacity='0.1'%3E%3Cpath d='m36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}
      ></div>
      
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden relative z-10">
        {/* Header */}
        <div 
          className="px-8 py-6 text-white transition-all duration-300"
          style={{ backgroundColor: theme.primary[500] }}
        >
          <div className="flex items-center space-x-3 mb-3">
            {selectedPortalData.icon}
            <h1 className="text-2xl font-bold">ConstructionAI</h1>
          </div>
          <p className="text-sm text-white/90 font-medium">{selectedPortalData.name}</p>
          <p className="text-xs text-white/70 mt-1">{selectedPortalData.description}</p>
        </div>

        <div className="p-8">
          {/* Portal Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select Portal
            </label>
            <div className="grid grid-cols-2 gap-3">
              {portals.map((portal) => (
                <button
                  key={portal.id}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, selectedPortal: portal.id }))}
                  className={`p-4 rounded-lg border-2 transition-all duration-200 text-left ${
                    formData.selectedPortal === portal.id
                      ? `border-[${theme.primary[500]}] bg-blue-50 text-blue-700`
                      : 'border-gray-200 hover:border-gray-300 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <div className={`p-1.5 rounded-md ${
                      formData.selectedPortal === portal.id 
                        ? 'text-blue-600 bg-blue-100' 
                        : 'text-gray-400 bg-gray-100'
                    }`}>
                      {React.cloneElement(portal.icon, { className: "w-5 h-5" })}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="text-sm font-semibold truncate">{portal.name}</div>
                      <div className="text-xs text-gray-500 mt-0.5 leading-tight">
                        {portal.description.split(',')[0]}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:border-transparent transition-all duration-200"
                style={{ 
                  '--tw-ring-color': theme.primary[500] + '40',
                  focusRingColor: theme.primary[500] + '40'
                }}
                placeholder="your.email@company.com"
              />
            </div>

            {/* Password Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:border-transparent transition-all duration-200 pr-12"
                  style={{ 
                    '--tw-ring-color': theme.primary[500] + '40',
                    focusRingColor: theme.primary[500] + '40'
                  }}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Remember Device */}
            <div className="flex items-start">
              <input
                type="checkbox"
                name="rememberDevice"
                id="rememberDevice"
                checked={formData.rememberDevice}
                onChange={handleInputChange}
                className="w-4 h-4 mt-0.5 rounded border-gray-300 focus:ring-2"
                style={{ 
                  accentColor: theme.primary[500],
                  '--tw-ring-color': theme.primary[500] + '40'
                }}
              />
              <label htmlFor="rememberDevice" className="ml-3 text-sm text-gray-600">
                <span className="font-medium">Remember this device</span>
                <span className="block text-xs text-gray-400 mt-0.5">
                  Recommended for site tablets and trusted devices
                </span>
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 px-4 rounded-lg text-white font-semibold transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.01] active:scale-[0.99]"
              style={{ 
                backgroundColor: isLoading ? theme.secondary[400] : theme.primary[500],
                '&:hover': { backgroundColor: theme.primary[600] }
              }}
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Signing In...
                </div>
              ) : (
                'Sign In to Construction Portal'
              )}
            </button>
          </form>

          {/* Footer Links */}
          <div className="mt-6 text-center space-y-3">
            <a 
              href="#" 
              className="text-sm font-medium hover:underline transition-colors"
              style={{ color: theme.primary[600] }}
            >
              Forgot Password?
            </a>
            <div className="flex items-center justify-center space-x-2 text-xs text-gray-500">
              <Shield className="w-3 h-3 text-red-500" />
              <span>Emergency:</span>
              <a 
                href="tel:+15551234567" 
                className="text-red-600 font-semibold hover:text-red-800 hover:underline"
              >
                (555) 123-4567
              </a>
            </div>
          </div>
        </div>

        {/* Security Footer */}
        <div className="bg-gray-50 px-8 py-4 border-t border-gray-100">
          <div className="flex items-center justify-center space-x-2 text-xs text-gray-500">
            <Shield className="w-3 h-3 text-green-600" />
            <span>Secure SSL Connection</span>
            <span>•</span>
            <span>Safety First Technology</span>
          </div>
        </div>
      </div>

      {/* Demo Info Card */}
      <div className="fixed bottom-6 right-6 bg-white/95 backdrop-blur-sm rounded-lg p-4 shadow-lg border border-gray-200 max-w-sm">
        <h3 className="font-bold text-gray-800 text-sm mb-2 flex items-center">
          <Shield className="w-4 h-4 mr-2" style={{ color: theme.primary[500] }} />
          Demo Wireframe
        </h3>
        <div className="space-y-2 text-xs text-gray-600">
          <div><span className="font-medium">Email:</span> j.wilson@skylineconstruction.com</div>
          <div><span className="font-medium">Password:</span> demo123</div>
          <div className="text-xs text-gray-500 pt-1 border-t border-gray-200">
            Choose any portal to explore different user experiences with brilliant mock data
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;