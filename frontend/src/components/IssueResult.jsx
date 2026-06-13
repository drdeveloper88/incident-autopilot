import React from 'react';
import './IssueResult.css';

function IssueResult({ issue }) {
  if (!issue) {
    return <div className="no-issue">No issue selected</div>;
  }

  const getStatusColor = (status) => {
    return status ? 'resolved' : 'pending';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'high';
    if (confidence >= 0.5) return 'medium';
    return 'low';
  };

  return (
    <div className="issue-result">
      <div className="result-header">
        <div className="issue-title-section">
          <h2>{issue.description}</h2>
          <div className="issue-meta">
            <span className={`badge severity-${issue.severity}`}>
              {issue.severity === 'high'
                ? '🔴 HIGH'
                : issue.severity === 'medium'
                ? '🟡 MEDIUM'
                : '🟢 LOW'}
            </span>
            <span className={`badge status-${getStatusColor(issue.is_resolved)}`}>
              {issue.is_resolved ? '✅ RESOLVED' : '⏳ PENDING'}
            </span>
          </div>
        </div>
        <div className="issue-id">
          <small>ID: {issue.issue_id}</small>
        </div>
      </div>

      <div className="results-grid">
        {/* Root Cause Section */}
        <div className="result-card">
          <div className="card-header">
            <h3>🔍 Root Cause Analysis</h3>
            <span className={`confidence ${getConfidenceColor(issue.analysis_confidence)}`}>
              {(issue.analysis_confidence * 100).toFixed(1)}% Confidence
            </span>
          </div>
          <div className="card-content">
            <p>{issue.root_cause || 'Analysis in progress...'}</p>
          </div>
        </div>

        {/* Remediation Steps Section */}
        <div className="result-card">
          <div className="card-header">
            <h3>✅ Remediation Steps</h3>
            <span className="step-count">{issue.remediation_steps?.length || 0} steps</span>
          </div>
          <div className="card-content">
            {issue.remediation_steps && issue.remediation_steps.length > 0 ? (
              <ol className="steps-list">
                {issue.remediation_steps.map((step, index) => (
                  <li key={index}>
                    <span className="step-number">{index + 1}</span>
                    <span className="step-text">{step}</span>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="empty">No remediation steps available</p>
            )}
          </div>
        </div>

        {/* Assignment Section */}
        {issue.assigned_to && (
          <div className="result-card">
            <div className="card-header">
              <h3>👤 Assigned To</h3>
            </div>
            <div className="card-content">
              <div className="assigned-to">
                <span className="avatar">{issue.assigned_to.charAt(0).toUpperCase()}</span>
                <span className="name">{issue.assigned_to}</span>
              </div>
            </div>
          </div>
        )}

        {/* Execution Metrics */}
        {issue.execution_metrics && Object.keys(issue.execution_metrics).length > 0 && (
          <div className="result-card">
            <div className="card-header">
              <h3>⏱️ Execution Metrics</h3>
            </div>
            <div className="card-content">
              <div className="metrics-list">
                {Object.entries(issue.execution_metrics).map(([step, data]) => (
                  <div key={step} className="metric-item">
                    <span className="metric-label">{step}:</span>
                    <span className="metric-value">
                      {data.duration?.toFixed(2)}s
                      <span className={`status-dot ${data.status}`}></span>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Timeline Section */}
      <div className="timeline-section">
        <h3>📅 Timeline</h3>
        <div className="timeline">
          <div className="timeline-item">
            <div className="timeline-marker"></div>
            <div className="timeline-content">
              <span className="timeline-time">Created</span>
              <span className="timeline-date">
                {new Date(issue.created_at).toLocaleString()}
              </span>
            </div>
          </div>
          {issue.updated_at !== issue.created_at && (
            <div className="timeline-item">
              <div className="timeline-marker"></div>
              <div className="timeline-content">
                <span className="timeline-time">Last Updated</span>
                <span className="timeline-date">
                  {new Date(issue.updated_at).toLocaleString()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Error Section */}
      {issue.error && (
        <div className="error-section">
          <h3>⚠️ Error</h3>
          <p className="error-message">{issue.error}</p>
        </div>
      )}

      {/* Messages Section */}
      {issue.messages && issue.messages.length > 0 && (
        <div className="messages-section">
          <h3>📝 Processing Log</h3>
          <div className="messages-list">
            {issue.messages.map((msg, index) => (
              <div key={index} className="message-item">
                <span className="msg-step">{msg.step}</span>
                <span className="msg-time">{(msg.duration_seconds || 0).toFixed(2)}s</span>
                <span className="msg-timestamp">
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default IssueResult;
