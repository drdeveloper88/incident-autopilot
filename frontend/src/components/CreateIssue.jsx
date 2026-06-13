import React, { useState } from 'react';
import './CreateIssue.css';

// API configuration
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function CreateIssue({ onIssueCreated }) {
  const [description, setDescription] = useState('');
  const [severity, setSeverity] = useState('medium');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!description.trim()) {
      setError('Please describe the issue');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/issues`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description: description.trim(),
          severity: severity,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      setSuccessMessage('✅ Ticket created and analyzed successfully!');
      setDescription('');
      setSeverity('medium');
      
      // Call parent callback
      onIssueCreated(data);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(`Failed to create ticket: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-issue-container">
      <div className="form-wrapper">
        <h2>📝 Create New Ticket</h2>
        <p className="form-subtitle">Describe the issue and let AI analyze it</p>

        <form onSubmit={handleSubmit} className="issue-form">
          <div className="form-group">
            <label htmlFor="description">Issue Description *</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Example: Database connection timeout on production server..."
              rows="6"
              disabled={loading}
            />
            <small>Provide detailed information about the issue</small>
          </div>

          <div className="form-group">
            <label htmlFor="severity">Severity Level</label>
            <select
              id="severity"
              value={severity}
              onChange={(e) => setSeverity(e.target.value)}
              disabled={loading}
            >
              <option value="low">🟢 Low - Minor issue</option>
              <option value="medium">🟡 Medium - Standard issue</option>
              <option value="high">🔴 High - Critical issue</option>
            </select>
          </div>

          {error && <div className="alert alert-error">{error}</div>}
          {successMessage && <div className="alert alert-success">{successMessage}</div>}

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? '⏳ Processing...' : '🚀 Analyze & Process'}
          </button>
        </form>

        <div className="form-hints">
          <h3>💡 Ticket Examples</h3>
          <div className="hint-list">
            <div className="hint-item">
              <strong>Technical Issue:</strong> "API endpoint returning 500 errors after deployment"
            </div>
            <div className="hint-item">
              <strong>Performance:</strong> "Database queries taking 30+ seconds on main dashboard"
            </div>
            <div className="hint-item">
              <strong>Feature Request:</strong> "User authentication integration with OAuth"
            </div>
          </div>
        </div>
      </div>

      <div className="form-info">
        <div className="info-card">
          <h3>🤖 AI Analysis Includes</h3>
          <ul>
            <li>Root cause identification</li>
            <li>Remediation steps</li>
            <li>Solution validation</li>
            <li>Developer assignment</li>
            <li>Confidence scoring</li>
          </ul>
        </div>

        <div className="info-card">
          <h3>⚡ Processing Steps</h3>
          <ol>
            <li>Issue analysis</li>
            <li>Solution generation</li>
            <li>Validation check</li>
            <li>Developer assignment (if needed)</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default CreateIssue;
