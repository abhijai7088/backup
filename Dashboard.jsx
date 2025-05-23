import React from "react";
import MapOverview from "./MapOverlay";
import ConfirmationBox from "./ConfirmationBox";
import VehiclePanel from "./VehiclePanel";
import './Dashboard.css';

const Dashboard = () => {
  const tracks = [
    { id: "TL-15B-756", status: "On Time" },
    { id: "TL-15B-746", status: "On Time" },
    { id: "TL-4E-8", status: "Delayed" },
    { id: "TL-15B-746", status: "On Time" },
    { id: "TL-15B-746", status: "On Time" },
    { id: "TL-15B-746", status: "On Time" }
  ];

  return (
    <div className="dashboard-container">
      {/* Map Layer */}
      <div className="dashboard-maparea">
        <MapOverview />
      </div>

      {/* Top Nav */}
      <div className="dashboard-topnav">
        Hyper-Tensor OS
      </div>

      {/* Layout */}
      <div className="dashboard-body">
        {/* Sidebar */}
        <div className="dashboard-sidebar">
          <div className="sidebar-heading">Route Planner</div>
          <div className="sidebar-form">
            <input placeholder="Origin" className="sidebar-input" />
            <select className="sidebar-input">
              <option>Halts</option>
            </select>
            <input placeholder="Destination" className="sidebar-input" />
          </div>

          <div className="sidebar-checklist">
            <div className="checklist-title">Checklist</div>
            <div className="checklist-item">
              <span>Personnels</span><span className="status-ok">✔️</span>
            </div>
            <div className="checklist-item">
              <span>Equipments</span><span className="status-ok">✔️</span>
            </div>
            <div className="checklist-item">
              <span>Commodities</span><span className="status-warn">⚠️</span>
            </div>
            <button className="generate-button">Generate Plan</button>
          </div>
        </div>

        {/* Tracks Panel */}
        <div className="tracks-panel">
          <div className="tracks-title">Tracks</div>
          {tracks.map((track, idx) => (
            <div
              key={idx}
              className={`track-box ${track.status === "Delayed" ? "track-delayed" : "track-ontime"}`}
            >
              <div className="track-id">Convoy: {track.id}</div>
              <div>Meerut - TCP8</div>
              <div>Status: <span className={track.status === "Delayed" ? "status-warn" : "status-ok"}>{track.status}</span></div>
            </div>
          ))}
        </div>
      </div>

      {/* Floating Panels */}
      <ConfirmationBox />
      <div className="vehicle-panel-wrapper">
        <VehiclePanel />
      </div>
    </div>
  );
};

export default Dashboard;
