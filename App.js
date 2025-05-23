// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SplashScreen from './SplashScreen';
import OrchestrationPage from './pages/OrchestrationPage';
import RoutePlanner from './components/RoutePlanner';
import Dashboard from "./components/Dashboard";
import VehiclePanel from './components/VehiclePanel';

import './index.css'; // This should point to the file where @tailwind is declared

function App() {
  return (
    <>
      
      <Router>
        <Routes>
          <Route path="/" element={<SplashScreen />} />
          <Route path="/Dashboard" element={<Dashboard />} />
          {/* <Route path="/ActionPopup" element={<OrchestrationPage />} /> */}
          {/* <Route path="/VehiclePanel" element={<VehiclePanel />} /> */}
          {/* <Route path="/MapOverlay" element={<OrchestrationPage />} /> */}
          {/* <Route path="/ConfirmationBox" element={<OrchestrationPage />} /> */}
          <Route path="/mission-planner" element={<RoutePlanner />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
