import React, { useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import '../components/planner.css';
import ActionPopup from './ActionPopup';

mapboxgl.accessToken = 'pk.eyJ1IjoidXR0a2Fyc2gxNCIsImEiOiJjbWF2NW1wOXMwMHp6MmtyMm0zNXV0Z3lyIn0.WmE75TOX8kwUuHk4Gi_pww';

const fuelFactors = {
  'military-jeep': 0.6,
  'transport-tank': 0.8,
  'battle-tank': 1.2,
  'artillery-vehicle': 1.5,
  'apc': 1.0
};

const speedByVehicle = {
  'military-jeep': 60,
  'transport-tank': 50,
  'battle-tank': 40,
  'artillery-vehicle': 35,
  'apc': 55
};

let currentRoutes = [];
let map;

const RoutePlanner = () => {
  const [showPopup, setShowPopup] = useState(false);



  useEffect(() => {
    map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/dark-v10',
      center: [77.209, 28.6139],
      zoom: 4
    });

    map.addControl(new mapboxgl.NavigationControl());

    const handlePlan = async () => {
      const start = document.getElementById('start').value.trim();
      const end = document.getElementById('end').value.trim();
      const payload = parseInt(document.getElementById('load').value.trim()) || 1000;
      const vehicle = document.getElementById('vehicle').value;

      if (!start || !end) return alert('Please enter both start and end locations.');

        if (isNaN(payload) || payload <= 0) return alert('Please enter a valid load in kg.');

      try {
        const [startCoords, endCoords] = await Promise.all([
          geocodeLocation(start),
          geocodeLocation(end)
        ]);

        const routes = await getRoutes(startCoords, endCoords);

        clearRoutes();
        addMarkers(startCoords, endCoords);

        // Add 9-second delay before displaying routes just to do the loading animation ----abhi
        setTimeout(() => {
          displayTopRoutes(routes, payload, vehicle);
          window.routes = routes;
          setShowPopup(false); // Hide popup after delay ----abhi
        }, 9000);

      } catch (err) {
        alert(err.message);
        setShowPopup(false);
      }
    };

    document.getElementById('planBtn').addEventListener('click', handlePlan);

    return () => {
      if (map) map.remove();
    };
  }, []);

  return (
    <div className="container">
      {showPopup && <ActionPopup onClose={() => setShowPopup(false)} animated />}

      <aside className="control-panel">
        <h2 title="Plan strategic military missions with optimal routes">🪖 Mission Route Planner</h2>
        <label htmlFor="start">📍 Start Location</label>
        <input type="text" id="start" placeholder="e.g. Delhi" title="Enter starting location" />

        <label htmlFor="end">🏁 End Location</label>
        <input type="text" id="end" placeholder="e.g. Chandigarh" title="Enter destination location" />

        <label htmlFor="vehicle">🚗 Vehicle Type</label>
        <select id="vehicle" title="Choose vehicle type">
          <option value="military-jeep">🚙 Military Jeep</option>
          <option value="transport-tank">🚚 Transport Tank</option>
          <option value="battle-tank">🛡️ Battle Tank</option>
          <option value="apc">🚓 Armored Personnel Carrier</option>
          <option value="artillery-vehicle">🧨 Artillery Vehicle</option>
        </select>

        <label htmlFor="load">⚖️ Load (kg)</label>
        <input type="number" id="load" placeholder="e.g. 1200" title="Weight load in kilograms" />

        <label htmlFor="priority">Mission Priority</label>
        <select id="priority" defaultValue="medium">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>

        <button id="planBtn" title="Calculate optimal route">🚀 Plan Route</button>
      </aside>

      <main className="map-section">
        <div id="map" title="Map showing planned military route"></div>
        <section className="comparison-panel" title="Shows route details">
          <h3>🧭 Route Comparison</h3>
          <div id="route-comparison"></div>
        </section>
      </main>
    </div>
  );
};

async function geocodeLocation(locationName) {
  const response = await fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(locationName)}.json?access_token=${mapboxgl.accessToken}`);
  const data = await response.json();
  if (data.features?.length) return data.features[0].center;
  throw new Error(`Location "${locationName}" not found.`);
}

async function getRoutes(startCoords, endCoords) {
  const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${startCoords[0]},${startCoords[1]};${endCoords[0]},${endCoords[1]}?alternatives=true&geometries=geojson&overview=full&access_token=${mapboxgl.accessToken}`;
  const response = await fetch(url);
  const data = await response.json();
  if (data.routes?.length) return data.routes;
  throw new Error('No routes found.');
}

function clearRoutes() {
  currentRoutes.forEach(route => {
    if (map.getLayer(route.id)) map.removeLayer(route.id);
    if (map.getSource(route.id)) map.removeSource(route.id);
  });
  currentRoutes = [];
}

function addMarkers(startCoords, endCoords) {
  if (window.startMarker) window.startMarker.remove();
  if (window.endMarker) window.endMarker.remove();

  window.startMarker = new mapboxgl.Marker({ color: 'green' }).setLngLat(startCoords).addTo(map);
  window.endMarker = new mapboxgl.Marker({ color: 'red' }).setLngLat(endCoords).addTo(map);
}

function calculateFuel(distance, payload, vehicleType) {
  const baseFuel = distance * 0.5;
  const loadFactor = 1 + (payload - 1000) / 2000;
  const fuelFactor = fuelFactors[vehicleType] || 1.0;
  return Math.round(baseFuel * loadFactor * fuelFactor);
}

function calculateETA(distance, vehicleType) {
  const speed = speedByVehicle[vehicleType] || 50;
  return +(distance / speed).toFixed(2);
}

function displayTopRoutes(routes, payload, vehicleType) {
  const comparisonDiv = document.getElementById('route-comparison');
  comparisonDiv.innerHTML = '';

  const topRoutes = routes.slice(0, 4);
  const bounds = new mapboxgl.LngLatBounds();

  topRoutes.forEach((route, i) => {
    const id = `route-${Date.now()}-${i}`;
    currentRoutes.push({ id, route });

    map.addSource(id, {
      type: 'geojson',
      data: {
        type: 'Feature',
        geometry: route.geometry
      }
    });

    map.addLayer({
      id,
      type: 'line',
      source: id,
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': i === 0 ? '#10b981' : '#3b82f6',
        'line-width': i === 0 ? 5 : 3,
        'line-opacity': 0.8
      }
    });

    route.geometry.coordinates.forEach(coord => bounds.extend(coord));

    const distance = route.distance / 1000;
    const fuel = calculateFuel(distance, payload, vehicleType);
    const eta = calculateETA(distance, vehicleType);

    const box = document.createElement('div');
    box.className = 'route-box';
    box.innerHTML = `
      <strong>Route ${i + 1}</strong><br/>
      Fuel Required: ${fuel} L<br/>
      Distance: ${distance.toFixed(2)} km<br/>
      ETA: ${eta} hrs<br/>
      Vehicle Type: ${vehicleType}<br/>
      Load: ${payload} kg
      <br/><button onclick="window.highlightRoute(${i})">Select Route</button>
    `;
    comparisonDiv.appendChild(box);
  });

  map.fitBounds(bounds, { padding: 50 });
}

window.highlightRoute = function (index) {
  const selectedRoute = currentRoutes[index].route;
  const routeBounds = new mapboxgl.LngLatBounds();
  selectedRoute.geometry.coordinates.forEach(coord => routeBounds.extend(coord));
  map.fitBounds(routeBounds, { padding: 100 });

  currentRoutes.forEach((r, i) => {
    map.setPaintProperty(r.id, 'line-color', i === index ? '#ffffff' : '#3b82f6');
    map.setPaintProperty(r.id, 'line-width', i === index ? 6 : 2);
    map.setPaintProperty(r.id, 'line-opacity', i === index ? 1 : 0.3);
  });
};

export default RoutePlanner;
