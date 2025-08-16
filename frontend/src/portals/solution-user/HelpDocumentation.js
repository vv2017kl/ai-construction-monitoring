import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { 
  HelpCircle, Search, Book, Video, MessageSquare, Star,
  ChevronRight, ChevronLeft, ExternalLink, Download, Share2,
  ThumbsUp, ThumbsDown, Flag, Play, Bookmark, FileText,
  Lightbulb, AlertCircle, CheckCircle, ArrowLeft, Filter,
  User, Camera, Shield, Settings, BarChart3, Clock, Map
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../../components/shared/Layout/MainLayout';

const HelpDocumentation = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { theme } = useTheme();
  const { user } = useAuth();
  
  // Role-based content management
  const isAdmin = user?.role === 'admin' || user?.role === 'system_administrator';
  const isManager = user?.role === 'site_manager' || user?.role === 'site_supervisor';
  const isWorker = user?.role === 'site_worker' || user?.role === 'equipment_operator';
  
  const [searchTerm, setSearchTerm] = useState(searchParams.get('search') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'all');
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState({});

  // Role-based help categories
  const getHelpCategories = () => {
    const baseCategories = [
      { id: 'getting-started', label: 'Getting Started', icon: Play, color: 'bg-green-100 text-green-800' },
      { id: 'safety', label: 'Safety Guidelines', icon: Shield, color: 'bg-red-100 text-red-800' },
      { id: 'cameras', label: 'Camera System', icon: Camera, color: 'bg-blue-100 text-blue-800' }
    ];
    
    if (isManager || isAdmin) {
      baseCategories.push(
        { id: 'personnel', label: 'Personnel Management', icon: User, color: 'bg-purple-100 text-purple-800' },
        { id: 'reports', label: 'Reports & Analytics', icon: BarChart3, color: 'bg-orange-100 text-orange-800' }
      );
    }
    
    if (isAdmin) {
      baseCategories.push(
        { id: 'administration', label: 'System Administration', icon: Settings, color: 'bg-gray-100 text-gray-800' },
        { id: 'integrations', label: 'Integrations & API', icon: ExternalLink, color: 'bg-indigo-100 text-indigo-800' }
      );
    }
    
    return baseCategories;
  };

  // Mock help articles with role-based filtering
  const helpArticles = [
    // Getting Started - All Users
    {
      id: 1,
      title: 'Welcome to AI Construction Platform',
      category: 'getting-started',
      type: 'article',
      difficulty: 'beginner',
      readTime: '5 min',
      description: 'Learn the basics of navigating and using the AI Construction platform.',
      content: 'Welcome to the AI Construction platform. This guide will help you...',
      tags: ['basics', 'overview', 'navigation'],
      views: 1250,
      helpful: 45,
      unhelpful: 3,
      roles: ['all']
    },
    {
      id: 2,
      title: 'First Day on Site: Safety Checklist',
      category: 'safety',
      type: 'checklist',
      difficulty: 'beginner',
      readTime: '3 min',
      description: 'Essential safety checklist for new workers on construction sites.',
      content: 'Before starting work on any construction site...',
      tags: ['safety', 'checklist', 'ppe', 'new-workers'],
      views: 890,
      helpful: 62,
      unhelpful: 1,
      roles: ['site_worker', 'equipment_operator', 'all']
    },
    {
      id: 3,
      title: 'How to View Live Camera Feeds',
      category: 'cameras',
      type: 'tutorial',
      difficulty: 'beginner',
      readTime: '4 min',
      description: 'Step-by-step guide to accessing and viewing live camera feeds.',
      content: 'To access live camera feeds...',
      tags: ['cameras', 'live-view', 'monitoring'],
      views: 756,
      helpful: 38,
      unhelpful: 2,
      roles: ['all']
    },
    
    // Manager/Admin Content
    {
      id: 4,
      title: 'Managing Site Personnel and Roles',
      category: 'personnel',
      type: 'guide',
      difficulty: 'intermediate',
      readTime: '10 min',
      description: 'Complete guide to managing personnel, assigning roles, and tracking attendance.',
      content: 'Personnel management involves...',
      tags: ['personnel', 'roles', 'management', 'attendance'],
      views: 324,
      helpful: 28,
      unhelpful: 1,
      roles: ['site_manager', 'site_supervisor', 'admin']
    },
    {
      id: 5,
      title: 'Generating Site Safety Reports',
      category: 'reports',
      type: 'tutorial',
      difficulty: 'intermediate',
      readTime: '8 min',
      description: 'Learn how to generate comprehensive safety and compliance reports.',
      content: 'To generate safety reports...',
      tags: ['reports', 'safety', 'compliance', 'analytics'],
      views: 445,
      helpful: 31,
      unhelpful: 2,
      roles: ['site_manager', 'safety_inspector', 'admin']
    },
    
    // Admin Only Content
    {
      id: 6,
      title: 'System Configuration and Setup',
      category: 'administration',
      type: 'guide',
      difficulty: 'advanced',
      readTime: '15 min',
      description: 'Advanced system configuration for administrators.',
      content: 'System administration requires...',
      tags: ['administration', 'configuration', 'setup', 'advanced'],
      views: 156,
      helpful: 12,
      unhelpful: 0,
      roles: ['admin', 'system_administrator']
    },
    {
      id: 7,
      title: 'API Integration Guide',
      category: 'integrations',
      type: 'technical',
      difficulty: 'advanced',
      readTime: '20 min',
      description: 'Technical guide for integrating third-party systems via API.',
      content: 'API integration allows...',
      tags: ['api', 'integration', 'technical', 'developers'],
      views: 89,
      helpful: 8,
      unhelpful: 1,
      roles: ['admin', 'system_administrator']
    }
  ];

  // Filter articles based on user role
  const getFilteredArticles = () => {
    return helpArticles.filter(article => {
      // Role filtering
      const hasRoleAccess = article.roles.includes('all') || 
                           article.roles.includes(user?.role) ||
                           (isAdmin && article.roles.includes('admin')) ||
                           (isManager && article.roles.includes('site_manager'));
      
      // Category filtering
      const matchesCategory = selectedCategory === 'all' || article.category === selectedCategory;
      
      // Search filtering
      const matchesSearch = searchTerm === '' || 
                           article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           article.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           article.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
      
      return hasRoleAccess && matchesCategory && matchesSearch;
    });
  };

  const popularArticles = getFilteredArticles()
    .sort((a, b) => b.views - a.views)
    .slice(0, 5);

  const handleSearch = (term) => {
    setSearchTerm(term);
    setSearchParams({ search: term, category: selectedCategory });
  };

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
    setSearchParams({ search: searchTerm, category: category });
  };

  const handleFeedback = async (articleId, type) => {
    setFeedback(prev => ({ ...prev, [articleId]: type }));
    // API call to submit feedback
    console.log(`Feedback for article ${articleId}: ${type}`);
  };

  const ArticleCard = ({ article, compact = false }) => {
    const categoryInfo = getHelpCategories().find(cat => cat.id === article.category);
    const Icon = categoryInfo?.icon || FileText;
    
    return (
      <div 
        className={`border rounded-lg p-4 cursor-pointer transition-all ${
          theme === 'dark' 
            ? 'border-gray-600 hover:border-gray-500 bg-gray-800' 
            : 'border-gray-200 hover:border-gray-300 bg-white hover:bg-gray-50'
        } ${compact ? 'p-3' : ''}`}
        onClick={() => setSelectedArticle(article)}
      >
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Icon className="w-4 h-4 text-gray-500" />
            <span className={`text-xs px-2 py-1 rounded-full ${categoryInfo?.color || 'bg-gray-100 text-gray-800'}`}>
              {categoryInfo?.label || 'General'}
            </span>
            {article.difficulty && (
              <span className={`text-xs px-2 py-1 rounded-full ${
                article.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                article.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {article.difficulty}
              </span>
            )}
          </div>
          <ChevronRight className="w-4 h-4 text-gray-400" />
        </div>
        
        <h3 className={`font-medium mb-2 ${compact ? 'text-sm' : ''}`}>{article.title}</h3>
        <p className={`text-gray-600 mb-3 ${compact ? 'text-xs' : 'text-sm'}`}>{article.description}</p>
        
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center space-x-3">
            <span>{article.readTime}</span>
            <span>{article.views} views</span>
            <span>{article.helpful} helpful</span>
          </div>
          <div className="flex items-center space-x-1">
            {article.type === 'video' && <Video className="w-3 h-3" />}
            {article.type === 'tutorial' && <Play className="w-3 h-3" />}
            {article.type === 'checklist' && <CheckCircle className="w-3 h-3" />}
          </div>
        </div>
      </div>
    );
  };

  const ArticleViewer = ({ article }) => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <button 
          onClick={() => setSelectedArticle(null)}
          className="flex items-center space-x-2 text-blue-600 hover:text-blue-800"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Articles</span>
        </button>
        
        <div className="flex items-center space-x-2">
          <button className="p-2 text-gray-600 hover:text-gray-800">
            <Bookmark className="w-4 h-4" />
          </button>
          <button className="p-2 text-gray-600 hover:text-gray-800">
            <Share2 className="w-4 h-4" />
          </button>
          <button className="p-2 text-gray-600 hover:text-gray-800">
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      <div>
        <h1 className="text-3xl font-bold mb-4">{article.title}</h1>
        <div className="flex items-center space-x-4 text-sm text-gray-600 mb-6">
          <span>{article.readTime} read</span>
          <span>{article.views} views</span>
          <span>Updated 2 days ago</span>
        </div>
      </div>
      
      <div className="prose max-w-none">
        <p>{article.content}</p>
        {/* Article content would be rendered here */}
        <div className="bg-gray-50 p-6 rounded-lg mt-8">
          <h3>Need more help?</h3>
          <p>If this article didn't answer your question, you can:</p>
          <ul>
            <li>Contact support via the chat button</li>
            <li>Browse related articles</li>
            <li>Watch our video tutorials</li>
          </ul>
        </div>
      </div>
      
      <div className="border-t pt-6">
        <h3 className="font-medium mb-4">Was this article helpful?</h3>
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => handleFeedback(article.id, 'helpful')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              feedback[article.id] === 'helpful'
                ? 'bg-green-100 text-green-800 border border-green-300'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
            }`}
          >
            <ThumbsUp className="w-4 h-4" />
            <span>Helpful ({article.helpful})</span>
          </button>
          <button 
            onClick={() => handleFeedback(article.id, 'not-helpful')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              feedback[article.id] === 'not-helpful'
                ? 'bg-red-100 text-red-800 border border-red-300'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
            }`}
          >
            <ThumbsDown className="w-4 h-4" />
            <span>Not helpful ({article.unhelpful})</span>
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <MainLayout>
      <div className="p-6">
        {selectedArticle ? (
          <ArticleViewer article={selectedArticle} />
        ) : (
          <>
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <HelpCircle className="w-8 h-8 text-blue-600" />
                <div>
                  <h1 className="text-2xl font-bold">Help & Documentation</h1>
                  <p className="text-gray-600">
                    {isWorker ? 'Essential guides for safe and efficient work' :
                     isManager ? 'Management guides and best practices' :
                     'Comprehensive system documentation'}
                  </p>
                </div>
              </div>
              
              <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <MessageSquare className="w-4 h-4" />
                <span>Contact Support</span>
              </button>
            </div>

            {/* Search and Filters */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border p-4 mb-6">
              <div className="flex flex-col lg:flex-row lg:items-center space-y-4 lg:space-y-0 lg:space-x-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search help articles..."
                    value={searchTerm}
                    onChange={(e) => handleSearch(e.target.value)}
                    className={`w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                      theme === 'dark' 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300'
                    }`}
                  />
                </div>
                
                <div className="flex items-center space-x-2">
                  <Filter className="w-4 h-4 text-gray-500" />
                  <select
                    value={selectedCategory}
                    onChange={(e) => handleCategoryFilter(e.target.value)}
                    className={`px-3 py-2 border rounded-lg ${
                      theme === 'dark' 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300'
                    }`}
                  >
                    <option value="all">All Categories</option>
                    {getHelpCategories().map(category => (
                      <option key={category.id} value={category.id}>
                        {category.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Categories Sidebar */}
              <div className="lg:col-span-1">
                <div className="space-y-4">
                  {/* Quick Access for Workers */}
                  {isWorker && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h3 className="font-medium text-blue-900 mb-2">Quick Start</h3>
                      <div className="space-y-2 text-sm">
                        <button className="text-blue-700 hover:text-blue-900 block">Safety Guidelines</button>
                        <button className="text-blue-700 hover:text-blue-900 block">Camera Basics</button>
                        <button className="text-blue-700 hover:text-blue-900 block">PPE Requirements</button>
                      </div>
                    </div>
                  )}

                  {/* Categories */}
                  <div className="bg-white dark:bg-gray-800 rounded-lg border p-4">
                    <h3 className="font-medium mb-4">Categories</h3>
                    <div className="space-y-2">
                      {getHelpCategories().map(category => {
                        const Icon = category.icon;
                        const count = getFilteredArticles().filter(a => a.category === category.id).length;
                        return (
                          <button
                            key={category.id}
                            onClick={() => handleCategoryFilter(category.id)}
                            className={`w-full flex items-center justify-between p-2 rounded-lg text-left transition-colors ${
                              selectedCategory === category.id
                                ? 'bg-blue-50 text-blue-700'
                                : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                            }`}
                          >
                            <div className="flex items-center space-x-3">
                              <Icon className="w-4 h-4" />
                              <span className="text-sm">{category.label}</span>
                            </div>
                            <span className="text-xs text-gray-500">{count}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Popular Articles */}
                  <div className="bg-white dark:bg-gray-800 rounded-lg border p-4">
                    <h3 className="font-medium mb-4">Most Popular</h3>
                    <div className="space-y-3">
                      {popularArticles.slice(0, 3).map(article => (
                        <div key={article.id} className="cursor-pointer" onClick={() => setSelectedArticle(article)}>
                          <h4 className="text-sm font-medium hover:text-blue-600 transition-colors line-clamp-2">
                            {article.title}
                          </h4>
                          <p className="text-xs text-gray-500 mt-1">{article.views} views</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Main Content */}
              <div className="lg:col-span-3">
                <div className="space-y-6">
                  {/* Featured Content for New Users */}
                  {isWorker && (
                    <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg p-6">
                      <div className="flex items-center space-x-3 mb-4">
                        <Lightbulb className="w-6 h-6" />
                        <h3 className="text-xl font-semibold">New to the Platform?</h3>
                      </div>
                      <p className="mb-4 opacity-90">
                        Start with our essential safety guidelines and platform basics to get up and running safely.
                      </p>
                      <button 
                        onClick={() => setSelectedArticle(helpArticles.find(a => a.id === 2))}
                        className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                      >
                        View Safety Checklist
                      </button>
                    </div>
                  )}

                  {/* Search Results */}
                  {searchTerm && (
                    <div>
                      <h2 className="text-xl font-semibold mb-4">
                        Search Results for "{searchTerm}" ({getFilteredArticles().length})
                      </h2>
                    </div>
                  )}

                  {/* Articles Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {getFilteredArticles().map(article => (
                      <ArticleCard key={article.id} article={article} />
                    ))}
                  </div>

                  {getFilteredArticles().length === 0 && (
                    <div className="text-center py-12">
                      <HelpCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">No articles found</h3>
                      <p className="text-gray-600">
                        Try adjusting your search terms or browse by category.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </MainLayout>
  );
};

export default HelpDocumentation;