"""Quick start guide."""

# Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
cp .env.example .env

# Configure .env with your API keys
# GROQ_API_KEY from https://console.groq.com
# JIRA credentials
# SPLUNK credentials  
# DYNATRACE credentials

# Run application
python -m uvicorn src.api.main:app --reload

# API Docs
# http://localhost:8000/docs

# Health Check
curl http://localhost:8000/health

# Analyze Issue
curl -X POST http://localhost:8000/api/v1/issues/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "HOSP-001",
    "description": "Database connection timeout",
    "severity": "high"
  }'

# Get Stats
curl http://localhost:8000/api/v1/stats
