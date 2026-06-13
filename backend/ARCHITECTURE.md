# Architecture Overview

## System Design

```
┌──────────────────────────────────────────────────────────────┐
│                        FastAPI Server                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               REST API Endpoints                        │ │
│  │  - POST /api/v1/issues/analyze                         │ │
│  │  - GET /api/v1/issues/{id}                             │ │
│  │  - Webhooks (Jira, Splunk, Dynatrace)                  │ │
│  └──────────────────────┬──────────────────────────────────┘ │
│                         │                                     │
│  ┌──────────────────────▼──────────────────────────────────┐ │
│  │           LangGraph Workflow Execution                  │ │
│  │                                                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │ │
│  │  │ Analyze  │→ │ Resolve  │→ │ Validate │             │ │
│  │  │  Step    │  │   Step   │  │   Step   │             │ │
│  │  └──────────┘  └──────────┘  └────┬─────┘             │ │
│  │                                    │                   │ │
│  │                            ┌───────▼─────────┐         │ │
│  │                            │ Is Resolved?    │         │ │
│  │                            │ YES: End        │         │ │
│  │                            │ NO: Assign      │         │ │
│  │                            └─────────────────┘         │ │
│  │                                                          │ │
│  └───────────────────────┬──────────────────────────────────┘ │
│                          │                                     │
│  ┌───────────────────────▼──────────────────────────────────┐ │
│  │              CrewAI Agent Execution                      │ │
│  │                                                          │ │
│  │  ┌─────────────┐  ┌──────────────┐                      │ │
│  │  │ Analyzer    │  │ Resolver     │                      │ │
│  │  │ Agent       │  │ Agent        │                      │ │
│  │  └─────────────┘  └──────────────┘                      │ │
│  │                                                          │ │
│  │  ┌─────────────┐  ┌──────────────┐                      │ │
│  │  │ Validator   │  │ Assignment   │                      │ │
│  │  │ Agent       │  │ Agent        │                      │ │
│  │  └─────────────┘  └──────────────┘                      │ │
│  │                                                          │ │
│  └───────────────────────┬──────────────────────────────────┘ │
│                          │                                     │
│  ┌───────────────────────▼──────────────────────────────────┐ │
│  │              FastMCP Tools Interface                     │ │
│  │                                                          │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │ │
│  │  │ get_issue│ │get_logs  │ │get_metrics │search_kb │   │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │ │
│  │                                                          │ │
│  └───────────────────────┬──────────────────────────────────┘ │
│                          │                                     │
└──────────────────────────┼─────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ┌───▼──┐          ┌────▼────┐      ┌─────▼────┐
    │ Jira │          │ Splunk  │      │Dynatrace │
    └──────┘          └─────────┘      └──────────┘
```

## Data Flow

1. **Issue Submission**
   - User submits issue via API or webhook
   - FastAPI validates and creates IssueCreate

2. **Workflow Execution**
   - LangGraph initializes IssueState
   - Routes through analysis → resolution → validation → assignment

3. **Agent Execution**
   - CrewAI agents execute tasks
   - Tools (FastMCP) fetch data from external services
   - LangChain LLM generates analysis and recommendations

4. **Response**
   - IssueResponse returned to client
   - Issue stored in memory (can be persisted to database)

## Key Patterns

### 1. Modular Agent Architecture
Each agent has a single responsibility:
- **Analyzer**: Extract insights from logs and metrics
- **Resolver**: Search KB and generate solutions
- **Validator**: Verify fixes work
- **Assignment**: Match to experts

### 2. LangGraph State Management
```python
IssueState {
    issue_id: str
    description: str
    root_cause: str
    analysis_confidence: float
    remediation_steps: list
    is_resolved: bool
    assigned_to: str
    messages: list
}
```

### 3. Tool Integration with FastMCP
Tools provide interfaces to:
- Issue tracking (Jira)
- Log aggregation (Splunk)
- APM (Dynatrace)
- Knowledge base

### 4. LLM Provider Flexibility
Support multiple LLM backends:
- Groq (fast, free)
- OpenAI (quality)
- Local (privacy)

## Extension Points

### Add New Agent
```python
# src/agents/new_agent.py
def create_new_agent() -> Agent:
    llm = ChatGroq(api_key=settings.groq_api_key, model="mixtral-8x7b-32768")
    return Agent(
        role="New Role",
        goal="New goal",
        backstory="New backstory",
        verbose=settings.crew_verbose,
        llm=llm,
        tools=[...],
    )
```

### Add New Tool
```python
# src/tools/new_tools.py
@mcp_server.tool()
def new_tool(param: str) -> dict:
    """Tool description."""
    return {"result": "value"}
```

### Add Workflow Step
```python
# src/workflows/issue_workflow.py
workflow.add_node("new_step", new_step_function)
workflow.add_edge("previous_step", "new_step")
```

## Scalability Considerations

**Current** (Development)
- In-memory issue store
- Single-threaded execution
- Mock external services

**Production Ready**
- Database persistence (PostgreSQL)
- Async task queue (Celery)
- Service integration
- Monitoring and observability
- Error handling and retries
- Rate limiting

## Security

- API key management via environment variables
- No secrets in logs
- Input validation with Pydantic
- Future: RBAC, audit logging
