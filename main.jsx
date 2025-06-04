import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // optional, but must exist if you're importing styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
