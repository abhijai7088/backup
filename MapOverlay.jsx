import React, { useRef, useEffect } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = 'pk.eyJ1IjoidXR0a2Fyc2gxNCIsImEiOiJjbWFpODAzbG0wNGUxMmlzaTlpYWgybTVuIn0.LweKduVrNZ0Bmo3D5nBjAw';

const MapOverview = ({ origin, destination }) => {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/navigation-night-v1', 
      center: origin || [77.2090, 28.6139], // Default center
      zoom: 5
    });

    return () => mapRef.current.remove();
  }, []);

  useEffect(() => {
    const drawRoute = async () => {
      if (!origin || !destination || !mapRef.current) return;

      const res = await fetch(
        `https://api.mapbox.com/directions/v5/mapbox/driving/${origin[0]},${origin[1]};${destination[0]},${destination[1]}?geometries=geojson&access_token=${mapboxgl.accessToken}`
      );
      const data = await res.json();
      const route = data.routes[0].geometry;

      if (mapRef.current.getSource('route')) {
        mapRef.current.getSource('route').setData({
          type: 'Feature',
          geometry: route,
        });
      } else {
        mapRef.current.addSource('route', {
          type: 'geojson',
          data: {
            type: 'Feature',
            geometry: route,
          }
        });

        mapRef.current.addLayer({
          id: 'route',
          type: 'line',
          source: 'route',
          layout: {
            'line-join': 'round',
            'line-cap': 'round',
          },
          paint: {
            'line-color': '#1DB954',
            'line-width': 4,
          }
        });
      }

      mapRef.current.flyTo({
        center: origin,
        zoom: 7,
        essential: true
      });
    };

    if (mapRef.current && mapRef.current.isStyleLoaded()) {
      drawRoute();
    } else if (mapRef.current) {
      mapRef.current.on('load', drawRoute);
    }
  }, [origin, destination]);

  return (
    <div
      ref={mapContainerRef}
      style={{
        width: '100%',
        height: '100%',
      }}
    />
  );
};

export default MapOverview;