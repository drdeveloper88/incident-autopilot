# Ticket Resolution AI - Enterprise Agentic System

A production-grade, enterprise-ready AI-powered ticket resolution system using agentic AI for real-time analysis, resolution, and developer assignment.

## Overview

Ticket Resolution AI is an enterprise-grade agentic AI system that automates the entire ticket lifecycle:
- **Real-time Analysis** - Analyze ticket descriptions to identify root causes
- **Intelligent Resolution** - Search knowledge base and generate remediation steps
- **Validation** - Verify resolution effectiveness using system metrics
- **Smart Assignment** - Route unresolved tickets to appropriate developers

## Technology Stack

- **CrewAI 0.35.3** - Multi-agent orchestration with specialized roles
- **LangGraph 0.0.52** - Stateful workflow management with conditional routing
- **LangChain** - LLM interactions and tool integration
- **FastMCP 0.1.0** - Model Context Protocol for tool exposure
- **FastAPI 0.104.1** - Production-grade HTTP API with async support
- **Groq mixtral-8x7b-32768** - Fast, efficient LLM inference
- **LangSmith** - Tracing, debugging, and monitoring
- **Pydantic 2.5.0** - Data validation and settings management

## Project Structure

```
src/
├── agents/                 # CrewAI agents (Analyzer, Resolver, Validator, Assignment)
│   ├── analyzer_agent.py
│   ├── resolver_agent.py
│   ├── validator_agent.py
│   └── assignment_agent.py
├── tasks/                  # CrewAI tasks (coordinated agent work)
│   ├── analyzer_task.py
│   ├── resolver_task.py
│   ├── validator_task.py
│   └── assignment_task.py
├── tools/                  # Tool implementations (knowledge base, metrics, logging)
│   ├── analyzer_tools.py       # Issue analysis tools
│   ├── resolver_tools.py       # Knowledge base search with real-time data
│   ├── validator_tools.py      # System metrics & resolution validation
│   ├── mcp_server.py           # FastMCP server (tool exposure)
│   └── mcp_client.py           # MCP client integration
├── workflows/              # LangGraph workflow orchestration
│   └── issue_workflow.py       # 4-step workflow: analyze → resolve → validate → assign
├── api/                    # FastAPI REST endpoints
│   └── main.py            # HTTP API with async support
├── config/                 # Configuration management
│   ├── settings.py         # Application settings (Pydantic BaseSettings)
│   ├── logger.py           # Centralized logging
│   └── langsmith.py        # LangSmith tracing configuration
├── schemas/                # Pydantic data models
│   └── issue.py           # IssueCreate, IssueResponse
└── data/                   # Real-time data files
    ├── knowledge_base.json      # 11 production KB articles
    ├── jira_issues.json         # Sample issue data
    ├── splunk_logs.json         # Log data for analysis
    └── dynatrace_metrics.json   # System metrics for validation
```

## Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run application**:
```bash
python -m uvicorn src.api.main:app --reload
```

API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/v1/issues/analyze` - Analyze issue
- `GET /api/v1/issues/{id}` - Get issue
- `GET /api/v1/issues` - List issues
- `GET /api/v1/stats` - Statistics
- `POST /webhook/jira` - Jira webhook
- `POST /webhook/splunk` - Splunk webhook
- `POST /webhook/dynatrace` - Dynatrace webhook

## Key Components

### Agents (src/agents/)
- **Analyzer**: Analyzes issues and identifies root causes
- **Resolver**: Generates remediation steps
- **Validator**: Validates issue resolution
- **Assignment**: Assigns issues to teams

### Tasks (src/tasks/)
- **Analyze Task**: Analyze issue
- **Resolve Task**: Generate solutions
- **Validate Task**: Verify fixes
- **Assignment Task**: Assign to developer

### Tools (src/tools/)
- **get_issue**: Fetch issue details from Jira
- **get_logs**: Get error logs from Splunk
- **get_metrics**: Get metrics from Dynatrace
- **search_kb**: Search knowledge base

### Workflows (src/workflows/)
- **IssueWorkflow**: Main LangGraph workflow
  1. Analyze issue
  2. Resolve (if possible)
  3. Validate fix
  4. Assign (if needed)

## Configuration

See `.env.example` for all options. Key variables:

- `LLM_PROVIDER`: groq, openai (default: groq)
- `GROQ_API_KEY`: Groq API key
- `CREW_VERBOSE`: Enable verbose logging
- `WORKFLOW_TIMEOUT`: Workflow timeout in seconds

## Development

```bash
# Format code
black src/

# Lint
ruff check src/

# Type check
mypy src/

# Run tests
pytest tests/ -v
```

## Next Steps

1. Implement real Jira/Splunk/Dynatrace integration
2. Add database persistence
3. Implement confidence-based auto-resolution
4. Add monitoring and alerting
5. Create tests for agents and workflows
6. Deploy to production

## License

MIT
