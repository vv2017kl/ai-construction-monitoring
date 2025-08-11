import { useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import { ThemeProvider } from "./context/ThemeContext";
import LoginPage from "./pages/LoginPage";

// Solution User Portal Components (Modular Structure)
import SolutionUserDashboard from "./portals/solution-user/Dashboard";
import SolutionUserLiveView from "./portals/solution-user/LiveView";
import SolutionUserLiveStreetView from "./portals/solution-user/LiveStreetView";
import SolutionUserVideoReview from "./portals/solution-user/VideoReview";
import SolutionUserSiteOverview from "./portals/solution-user/SiteOverview";
import SolutionUserAlertCenter from "./portals/solution-user/AlertCenter";
import SolutionUserAIAnalytics from "./portals/solution-user/AIAnalytics";
import SolutionUserTimeLapse from "./portals/solution-user/TimeLapse";
import SolutionUserPersonnelManagement from "./portals/solution-user/PersonnelManagement";
import SolutionUserReportsCenter from "./portals/solution-user/ReportsCenter";
import SolutionUserFieldAssessment from "./portals/solution-user/FieldAssessment";
import SolutionUserMyProfile from "./portals/solution-user/MyProfile";
import SolutionUserTimeComparison from "./portals/solution-user/TimeComparison";
import SolutionUserHistoricalStreetView from "./portals/solution-user/HistoricalStreetView";
import SolutionUserStreetViewComparison from "./portals/solution-user/StreetViewComparison";
import SolutionUserPathAdministration from "./portals/solution-user/PathAdministration";

// Solution Admin Portal Components
import AdminDashboard from "./portals/solution-admin/AdminDashboard";
import UserDirectory from "./portals/solution-admin/UserDirectory";
import DepartmentManagement from "./portals/solution-admin/DepartmentManagement";
import AccessControl from "./portals/solution-admin/AccessControl";
import SiteConfiguration from "./portals/solution-admin/SiteConfiguration";
import EquipmentManagement from "./portals/solution-admin/EquipmentManagement";
import AIModelManagement from "./portals/solution-admin/AIModelManagement";
import SystemMonitoring from "./portals/solution-admin/SystemMonitoring";
import IntegrationSettings from "./portals/solution-admin/IntegrationSettings";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const helloWorldApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      console.log(response.data.message);
    } catch (e) {
      console.error(e, `errored out requesting / api`);
    }
  };

  useEffect(() => {
    helloWorldApi();
  }, []);

  return (
    <div>
      <header className="App-header">
        <a
          className="App-link"
          href="https://emergent.sh"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img src="https://avatars.githubusercontent.com/in/1201222?s=120&u=2686cf91179bbafbc7a71bfbc43004cf9ae1acea&v=4" />
        </a>
        <p className="mt-5">ConstructionAI Monitoring System</p>
        <div className="mt-8">
          <a 
            href="/login" 
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors inline-block"
          >
            Access Construction Portal
          </a>
        </div>
      </header>
    </div>
  );
};

function App() {
  return (
    <ThemeProvider>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
            
            {/* Solution User Portal Routes */}
            <Route path="/dashboard" element={<SolutionUserDashboard />} />
            <Route path="/live-view" element={<SolutionUserLiveView />} />
            <Route path="/live-street-view" element={<SolutionUserLiveStreetView />} />
            <Route path="/video-review" element={<SolutionUserVideoReview />} />
            <Route path="/site-overview" element={<SolutionUserSiteOverview />} />
            <Route path="/alert-center" element={<SolutionUserAlertCenter />} />
            <Route path="/alert-center/:alertId" element={<SolutionUserAlertCenter />} />
            <Route path="/ai-analytics" element={<SolutionUserAIAnalytics />} />
            <Route path="/time-lapse" element={<SolutionUserTimeLapse />} />
            <Route path="/personnel" element={<SolutionUserPersonnelManagement />} />
            <Route path="/reports" element={<SolutionUserReportsCenter />} />
            <Route path="/field-assessment" element={<SolutionUserFieldAssessment />} />
            <Route path="/profile" element={<SolutionUserMyProfile />} />
            <Route path="/time-comparison" element={<SolutionUserTimeComparison />} />
            <Route path="/historical-street" element={<SolutionUserHistoricalStreetView />} />
            <Route path="/street-comparison" element={<SolutionUserStreetViewComparison />} />
            <Route path="/path-admin" element={<SolutionUserPathAdministration />} />
            
            {/* Solution Admin Portal Routes */}
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/users" element={<UserDirectory />} />
            <Route path="/admin/departments" element={<DepartmentManagement />} />
            <Route path="/admin/access-control" element={<AccessControl />} />
            <Route path="/admin/site-config" element={<SiteConfiguration />} />
            <Route path="/admin/equipment" element={<EquipmentManagement />} />
            <Route path="/admin/ai-models" element={<AIModelManagement />} />
            <Route path="/admin/monitoring" element={<SystemMonitoring />} />
            
            {/* Future Portal Routes will be added here */}
            {/* VMS User Portal: /vms/operations/* */}
            {/* VMS Admin Portal: /vms/admin/* */}
          </Routes>
        </BrowserRouter>
      </div>
    </ThemeProvider>
  );
}

export default App;
