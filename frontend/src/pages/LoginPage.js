import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Shield, Camera, MapPin, AlertTriangle } from 'lucide-react';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberDevice: false,
    selectedPortal: 'solution-user' // Default portal
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const portals = [
    {
      id: 'solution-user',
      name: 'Construction Portal',
      description: 'Site Managers, Safety Officers, Project Coordinators',
      icon: <Shield className="w-6 h-6" />,
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    {
      id: 'solution-admin',
      name: 'Admin Portal',
      description: 'Company Executives, System Administrators',
      icon: <MapPin className="w-6 h-6" />,
      color: 'bg-emerald-600 hover:bg-emerald-700'
    },
    {
      id: 'vms-user',
      name: 'VMS Operations',
      description: 'Security Personnel, Camera Operators',
      icon: <Camera className="w-6 h-6" />,
      color: 'bg-purple-600 hover:bg-purple-700'
    },
    {
      id: 'vms-admin',
      name: 'VMS Admin',
      description: 'IT Staff, VMS System Administrators',
      icon: <AlertTriangle className="w-6 h-6" />,
      color: 'bg-orange-600 hover:bg-orange-700'
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
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Navigate based on selected portal
      switch (formData.selectedPortal) {
        case 'solution-user':
          navigate('/dashboard');
          break;
        case 'solution-admin':
          navigate('/admin/dashboard');
          break;
        case 'vms-user':
          navigate('/vms/operations');
          break;
        case 'vms-admin':
          navigate('/vms/admin');
          break;
        default:
          navigate('/dashboard');
      }
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const selectedPortalData = portals.find(p => p.id === formData.selectedPortal);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex items-center justify-center p-4">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.05"%3E%3Cpath d="m36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20"></div>
      
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl overflow-hidden relative z-10">
        {/* Header */}
        <div className={`${selectedPortalData.color} px-8 py-6 text-white transition-all duration-300`}>
          <div className="flex items-center space-x-3 mb-2">
            {selectedPortalData.icon}
            <h1 className="text-2xl font-bold">ConstructionAI</h1>
          </div>
          <p className="text-sm text-white/80">{selectedPortalData.name}</p>
          <p className="text-xs text-white/60 mt-1">{selectedPortalData.description}</p>
        </div>

        <div className="p-8">
          {/* Portal Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Portal
            </label>
            <div className="grid grid-cols-2 gap-2">
              {portals.map((portal) => (
                <button
                  key={portal.id}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, selectedPortal: portal.id }))}
                  className={`p-3 rounded-lg border-2 transition-all duration-200 text-left ${
                    formData.selectedPortal === portal.id
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300 text-gray-600'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <div className={`p-1 rounded ${formData.selectedPortal === portal.id ? 'text-blue-600' : 'text-gray-400'}`}>
                      {React.cloneElement(portal.icon, { className: "w-4 h-4" })}
                    </div>
                    <div>
                      <div className="text-xs font-medium">{portal.name}</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                placeholder="your.email@company.com"
              />
            </div>

            {/* Password Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 pr-12"
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
            <div className="flex items-center">
              <input
                type="checkbox"
                name="rememberDevice"
                id="rememberDevice"
                checked={formData.rememberDevice}
                onChange={handleInputChange}
                className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
              />
              <label htmlFor="rememberDevice" className="ml-2 text-sm text-gray-600">
                Remember this device
                <span className="text-xs text-gray-400 block">Recommended for site tablets</span>
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 px-4 rounded-lg text-white font-medium transition-all duration-200 ${
                isLoading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : `${selectedPortalData.color} transform hover:scale-[1.02] active:scale-[0.98]`
              }`}
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Signing In...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Footer Links */}
          <div className="mt-6 text-center space-y-2">
            <a href="#" className="text-sm text-blue-600 hover:text-blue-800 transition-colors">
              Forgot Password?
            </a>
            <div className="flex items-center justify-center space-x-1 text-xs text-gray-500">
              <span>Emergency Contact:</span>
              <a href="tel:+1234567890" className="text-red-600 font-medium hover:text-red-800">
                (123) 456-7890
              </a>
            </div>
          </div>
        </div>

        {/* Security Footer */}
        <div className="bg-gray-50 px-8 py-4 border-t">
          <div className="flex items-center justify-center space-x-2 text-xs text-gray-500">
            <Shield className="w-3 h-3" />
            <span>Secure SSL Connection</span>
            <span>•</span>
            <span>Construction Safety First</span>
          </div>
        </div>
      </div>

      {/* Demo Credentials */}
      <div className="fixed bottom-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg border border-white/20 max-w-xs">
        <h3 className="font-semibold text-gray-800 text-sm mb-2">Demo Credentials</h3>
        <div className="space-y-1 text-xs text-gray-600">
          <div><span className="font-medium">Email:</span> demo@construction.com</div>
          <div><span className="font-medium">Password:</span> demo123</div>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Choose any portal to explore different user experiences
        </div>
      </div>
    </div>
  );
};

export default LoginPage;