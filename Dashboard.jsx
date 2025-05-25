import React from "react";
import MapOverview from "./MapOverlay";
import ConfirmationBox from "./ConfirmationBox";
import VehiclePanel from "./VehiclePanel";
import './Dashboard.css';

import routeImage from '../assets/image.png';
import bagIcon from '../assets/bag.png';
import alertIcon from '../assets/alert.png';
import commoditiesIcon from '../assets/commodities.png';
import equipmentIcon from '../assets/equipment.png';
import personnelIcon from '../assets/personnel.png';
import tickIcon from '../assets/tick.png';

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

      {/* Top Navigation */}
      <div className="dashboard-topnav">
        Hyper-Tensor OS
      </div>

      {/* Main Body */}
      <div className="dashboard-body">
        {/* Sidebar */}
        <div >
          

          <div className="sidebar-container">
          <div className="box-header">
                <img src={routeImage} alt="Route" className="icon" />
                <h2 className="heading">Route Planner</h2>
                <div className="status-dot green"></div>
              </div>
            {/* Route Planner */}
            <div className="box">
              

              <label className="label"><b>Origin</b></label>
              <input type="text" className="input" placeholder="Enter origin" />

              <label className="label"><b>Halts</b></label>
              <select className="input">
                <option>Halts</option>
                <option>Checkpoint A</option>
                <option>Checkpoint B</option>
              </select>

              <label className="label"><b>Destination</b></label>
              <input type="text" className="input" placeholder="Enter destination" />
            </div>
            <div className="box-header">
                <img src={bagIcon} alt="Bag" className="icon" />
                <h2 className="heading">Cargo Status</h2>
                <div className="status-dot blue"></div>
              </div>

            {/* Cargo Status */}
            <div className="box">
              

              <div className="cargo-status">
                {[
                  { label: "Personnels", icon: personnelIcon, statusIcon: tickIcon },
                  { label: "Equipments", icon: equipmentIcon, statusIcon: tickIcon },
                  { label: "Commodities", icon: commoditiesIcon, statusIcon: alertIcon },
                ].map((item, idx) => (
                  <div key={idx} className="cargo-item">
                    <img src={item.icon} alt={item.label} className="cargo-icon" />
                    <span className="cargo-label">{item.label}</span>
                    <img src={item.statusIcon} alt="Status" className="status-icon" />
                  </div>
                ))}
              </div>
            </div>
          </div>

          <button className="generate-button">Generate Plan</button>
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
              <div>
                Status:{" "}
                <span className={track.status === "Delayed" ? "status-warn" : "status-ok"}>
                  {track.status}
                </span>
              </div>
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
