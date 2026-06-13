import React from 'react';
import './HealthStatus.css';

function HealthStatus({ health, onRefresh }) {
  return (
    <div className="health-status">
      <div className="status-indicator">
        <div className={`status-dot ${health?.status === 'healthy' ? 'healthy' : 'error'}`}></div>
        <span className="status-text">
          {health?.status === 'healthy' ? 'System Healthy' : 'System Error'}
        </span>
      </div>
      <button className="refresh-button" onClick={onRefresh} title="Refresh health status">
        🔄
      </button>
    </div>
  );
}

export default HealthStatus;
