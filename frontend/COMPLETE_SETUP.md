# 🎯 Ticket Resolution AI - Complete Setup Guide

**Enterprise-grade Agentic AI system for real-time ticket analysis, resolution, and developer assignment**

## 🏗️ Project Structure

```
issue-resolution-agentic-platform/
├── src/                          # Backend Python code
│   ├── api/
│   │   └── main.py               # FastAPI application
│   ├── config/
│   │   ├── settings.py           # Configuration management
│   │   └── logger.py             # Logging setup
│   ├── workflows/
│   │   ├── sequential_issue_workflow.py
│   │   ├── approval_based_workflow.py
│   │   └── workflow_state.py     # TypedDict definitions
│   └── schemas/
│       └── issue.py              # Pydantic models
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
├── .env                          # Environment configuration
├── requirements.txt              # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Backend Setup (Python)

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

Key packages:
- FastAPI 0.136.3 - REST API framework
- Uvicorn 0.49.0 - ASGI server
- LangChain with Groq integration - LLM framework
- LangGraph 1.2.4 - Workflow orchestration
- Pydantic 2.13.4 - Data validation

#### 2. Configure Environment
Update `.env` with your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=mixtral-8x7b-32768
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

#### 3. Start Backend Server
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: `http://localhost:8000`

#### 4. Test Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-06-06T...",
  "workflow_ready": true
}
```

### Frontend Setup (React)

#### 1. Install Node Dependencies
```bash
cd frontend
npm install
```

#### 2. Start Development Server
```bash
npm start
```

Frontend will open at: `http://localhost:3000`

#### 3. Access Swagger API Documentation
```
http://localhost:8000/docs
```

## 📊 System Architecture

```
┌─────────────────────┐
│  React Frontend     │
│  (http://3000)      │
└──────────┬──────────┘
           │
           │ HTTP Requests
           ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│      (http://localhost:8000)            │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │    Issue Resolution Workflow     │  │
│  │                                  │  │
│  │  1. Analyze (Root Cause)        │  │
│  │  2. Resolve (Remediation Steps) │  │
│  │  3. Validate (Solution Check)   │  │
│  │  4. Assign (Dev Assignment)     │  │
│  └──────────────────────────────────┘  │
│                                         │
│  LLM: ChatGroq (Mixtral 8x7B)          │
│  Workflow: LangGraph                    │
└─────────────────────────────────────────┘
```

## 🔄 Workflow Process

### Sequential Workflow (Default)
```
INPUT (Issue Description)
       ↓
[ANALYZE] - LLM analyzes issue, identifies root cause
       ↓
[RESOLVE] - LLM generates remediation steps
       ↓
[VALIDATE] - LLM validates solution effectiveness
       ↓
CONDITION: Is issue resolved?
├─ YES → END (Return resolved status)
└─ NO → [ASSIGN] - AI assigns to developer
           ↓
          END
```

### Approval-Based Workflow
```
[ANALYZE] → [RESOLVE] → [APPROVAL] → [VALIDATE] → [ASSIGN]
```

## 📝 API Endpoints

### Health Check
```
GET /health
Response: { "status": "healthy", "workflow_ready": true }
```

### Create Issue (Main Endpoint)
```
POST /issues
Body: {
  "description": "Database connection timeout",
  "severity": "high"  # low, medium, high
}

Response: {
  "issue_id": "uuid",
  "description": "...",
  "root_cause": "Connection pool exhaustion",
  "remediation_steps": [...],
  "is_resolved": true,
  "assigned_to": "Alice",
  "analysis_confidence": 0.85,
  "execution_metrics": {...}
}
```

### Get Issue Result
```
GET /issues/{issue_id}
Response: Full issue data
```

## 🎨 Frontend Features

### Dashboard Tab
- System health status
- Statistics (total tickets, resolved, pending)
- Recent tickets list
- Click to view details

### Create Ticket Tab
- Issue description form
- Severity selector
- Example tickets
- Real-time feedback

### Results Tab
- Root cause analysis with confidence score
- Step-by-step remediation
- Developer assignment
- Execution metrics
- Processing timeline

## 🔐 Environment Variables

```env
# Groq LLM Configuration
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=mixtral-8x7b-32768
GROQ_TEMPERATURE=0.3

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO

# Optional: LangSmith Observability
# LANGSMITH_API_KEY=your_key
# LANGSMITH_PROJECT=ticket-resolution

# Optional: External Services
# JIRA_API_KEY=your_jira_key
# SPLUNK_API_KEY=your_splunk_key
```

## 📦 Key Technologies

### Backend
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **LangChain** - LLM framework
- **LangGraph** - Workflow orchestration
- **ChatGroq** - LLM inference
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI framework
- **React Hooks** - State management
- **Fetch API** - HTTP requests
- **CSS** - Styling (no external CSS frameworks)

## 🧪 Testing

### Backend API Testing
Use Swagger UI at: `http://localhost:8000/docs`

Or test with curl:
```bash
# Health check
curl http://localhost:8000/health

# Create issue
curl -X POST http://localhost:8000/issues \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Database timeout",
    "severity": "high"
  }'
```

### Frontend Testing
The frontend automatically tests connection to the backend on load.

## 📱 Responsive Design

- ✅ Desktop (1400px+) - Full layout
- ✅ Tablet (768px-1024px) - Adjusted grid
- ✅ Mobile (< 768px) - Single column

## 🚀 Production Deployment

### Backend (Azure App Service)
```bash
# Build production server
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Or use Gunicorn
gunicorn src.api.main:app -w 4 -b 0.0.0.0:8000
```

### Frontend (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy the 'build' folder
```

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'langchain'"**
```bash
pip install langchain==1.3.4 langchain-groq langgraph
```

**"GROQ_API_KEY not found"**
- Ensure .env file exists in project root
- Run: `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('GROQ_API_KEY'))"`

**"Workflow not initialized"**
- Backend may have crashed, restart with: `python -m uvicorn src.api.main:app --reload`
- Check logs for errors

### Frontend Issues

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**"Port 3000 already in use"**
```bash
PORT=3001 npm start
```

**"Cannot find module"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `src/api/main.py` | FastAPI application with endpoints |
| `src/workflows/sequential_issue_workflow.py` | Main workflow: analyze→resolve→validate→assign |
| `src/config/settings.py` | Configuration from .env |
| `frontend/src/App.jsx` | Main React component |
| `frontend/src/components/CreateIssue.jsx` | Ticket creation form |
| `frontend/src/components/IssueResult.jsx` | Results display |

## ✅ Verification Checklist

- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] Health endpoint returns `workflow_ready: true`
- [ ] Can create new ticket in frontend
- [ ] Can see analysis results
- [ ] No error messages in browser console
- [ ] No error messages in terminal

## 🎯 Next Steps

1. **Get Groq API Key** - Sign up at [console.groq.com](https://console.groq.com)
2. **Update .env** - Add your GROQ_API_KEY
3. **Start Backend** - Run `python -m uvicorn src.api.main:app --reload`
4. **Start Frontend** - Run `cd frontend && npm start`
5. **Create Tickets** - Use the web UI to submit issues
6. **View Results** - See AI analysis and recommendations

## 📖 Documentation

- [Backend README](./README.md)
- [Frontend README](./frontend/README.md)
- [Frontend Setup Guide](./FRONTEND_SETUP.md)

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Review error messages in console/terminal
3. Check API health: `http://localhost:8000/health`
4. Review logs for more details

## 🎉 You're Ready!

Your Ticket Resolution AI platform is now fully set up and ready to use. Start creating tickets and let AI handle the analysis!
