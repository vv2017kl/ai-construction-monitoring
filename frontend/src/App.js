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
            
            {/* Future Portal Routes will be added here */}
            {/* Solution Admin Portal: /admin/* */}
            {/* VMS User Portal: /vms/operations/* */}
            {/* VMS Admin Portal: /vms/admin/* */}
          </Routes>
        </BrowserRouter>
      </div>
    </ThemeProvider>
  );
}

export default App;
