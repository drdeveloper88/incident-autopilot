import React, { useState, useEffect } from 'react';
import './App.css';
import HealthStatus from './components/HealthStatus';
import CreateIssue from './components/CreateIssue';
import IssueResult from './components/IssueResult';

// API configuration
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [health, setHealth] = useState(null);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [issues, setIssues] = useState([]);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      const data = await response.json();
      setHealth(data);
    } catch (error) {
      console.error('Error checking health:', error);
      setHealth({ status: 'error', workflow_ready: false });
    }
  };

  const handleIssueCreated = (issue) => {
    setIssues([issue, ...issues]);
    setSelectedIssue(issue);
    setActiveTab('results');
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>🎯 Ticket Resolution AI</h1>
          <p>Enterprise-grade Agentic AI system for ticket analysis, resolution, and assignment</p>
        </div>
        <HealthStatus health={health} onRefresh={checkHealth} />
      </header>

      <nav className="app-nav">
        <button
          className={`nav-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button
          className={`nav-button ${activeTab === 'create' ? 'active' : ''}`}
          onClick={() => setActiveTab('create')}
        >
          ➕ Create Ticket
        </button>
        <button
          className={`nav-button ${activeTab === 'results' ? 'active' : ''}`}
          onClick={() => setActiveTab('results')}
          disabled={!selectedIssue}
        >
          📋 Results ({issues.length})
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'dashboard' && (
          <div className="tab-content">
            <div className="dashboard-grid">
              <div className="dashboard-card">
                <h2>📈 Overview</h2>
                <div className="stat">
                  <span className="stat-label">Total Tickets Processed:</span>
                  <span className="stat-value">{issues.length}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">System Status:</span>
                  <span className={`stat-value ${health?.status === 'healthy' ? 'healthy' : 'error'}`}>
                    {health?.status === 'healthy' ? '✅ Healthy' : '❌ Error'}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Workflow Ready:</span>
                  <span className={`stat-value ${health?.workflow_ready ? 'yes' : 'no'}`}>
                    {health?.workflow_ready ? '✅ Yes' : '❌ No'}
                  </span>
                </div>
              </div>

              <div className="dashboard-card">
                <h2>🚀 Quick Stats</h2>
                <div className="stat">
                  <span className="stat-label">Resolved Issues:</span>
                  <span className="stat-value">
                    {issues.filter(i => i.is_resolved).length}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Pending Assignment:</span>
                  <span className="stat-value">
                    {issues.filter(i => !i.is_resolved).length}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Avg Confidence:</span>
                  <span className="stat-value">
                    {issues.length > 0
                      ? (
                          (issues.reduce((sum, i) => sum + i.analysis_confidence, 0) /
                            issues.length) *
                          100
                        ).toFixed(1) + '%'
                      : 'N/A'}
                  </span>
                </div>
              </div>

              <div className="dashboard-card recent-issues">
                <h2>📋 Recent Tickets</h2>
                {issues.length === 0 ? (
                  <p className="empty-message">No tickets yet. Create one to get started!</p>
                ) : (
                  <ul>
                    {issues.slice(0, 5).map(issue => (
                      <li key={issue.issue_id} onClick={() => {
                        setSelectedIssue(issue);
                        setActiveTab('results');
                      }}>
                        <span className="issue-title">{issue.description.substring(0, 40)}...</span>
                        <span className={`issue-status ${issue.is_resolved ? 'resolved' : 'pending'}`}>
                          {issue.is_resolved ? '✅ Resolved' : '⏳ Pending'}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'create' && (
          <div className="tab-content">
            <CreateIssue onIssueCreated={handleIssueCreated} />
          </div>
        )}

        {activeTab === 'results' && selectedIssue && (
          <div className="tab-content">
            <IssueResult issue={selectedIssue} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Ticket Resolution AI Platform • Powered by LangChain + Groq • API: http://localhost:8000</p>
      </footer>
    </div>
  );
}

export default App;
