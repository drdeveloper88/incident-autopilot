# LangSmith Integration Guide

## Overview

HospitalAI now integrates with **LangSmith**, the platform for developing production-grade LLM applications. This enables:

- 🔍 **Tracing**: Monitor agent and LLM calls in real-time
- 🐛 **Debugging**: Inspect execution flows and identify issues
- 📊 **Evaluation**: Run experiments and measure agent performance
- 📈 **Analytics**: Analyze patterns and optimize outputs
- 🎯 **Datasets**: Manage test cases and evaluation datasets

## Architecture

```
HospitalAI Workflow
        ↓
LangSmith Tracer (src/config/langsmith.py)
        ↓
LangSmith Cloud Platform (https://smith.langchain.com)
        ↓
Dashboard & Analytics
```

## Setup

### 1. Get LangSmith API Key

1. Go to https://smith.langchain.com
2. Sign up or log in
3. Navigate to Settings → API Keys
4. Copy your API key

### 2. Set Environment Variables

```bash
# Required
export LANGSMITH_API_KEY="your-api-key-here"

# Optional (defaults shown)
export LANGSMITH_PROJECT="HospitalAI"
export LANGSMITH_TRACING_V2="true"
export LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
```

### 3. Install LangSmith

```bash
pip install langsmith
# Add to requirements.txt: langsmith>=0.1.0
```

## Configuration

### LangSmithConfig

Central configuration class:

```python
from src.config.langsmith import LangSmithConfig

# Check if configured
if LangSmithConfig.is_configured():
    print("LangSmith is ready to trace")

# Access configuration
print(LangSmithConfig.PROJECT)      # "HospitalAI"
print(LangSmithConfig.API_KEY)      # "your-key"
print(LangSmithConfig.TRACING_ENABLED)  # True
```

## Usage

### Basic Tracing

The workflow automatically traces all steps:

```python
from src.workflows.issue_workflow import create_issue_workflow

workflow = create_issue_workflow()

# Run workflow - all steps are traced to LangSmith
state = workflow.invoke({
    "issue_id": "HOSP-001",
    "description": "Database connection timeout",
    "severity": "Critical",
    # ... other fields
})
```

### Trace Data

Each workflow step logs trace data including:

**Analyze Step:**
- Issue ID and severity
- Tool calls (get_issue_details, get_error_logs, get_system_metrics)
- Root cause identified
- Analysis confidence score

**Resolve Step:**
- Root cause context
- Knowledge base searches
- Remediation steps generated
- Number of solutions found

**Validate Step:**
- Remediation steps count
- System metrics retrieved
- Validation results
- Resolution status (True/False)

**Assign Step:**
- Issue severity and priority
- Developer assignment logic
- Assigned developer name
- Assignment reason

### Custom Tracing

Add tracing to your own functions:

```python
from src.config.langsmith import LangSmithTracer, LangSmithConfig

@LangSmithTracer.trace_agent_call("MyAgent", "Analyze data")
def analyze_data(data):
    # Your code here
    pass

# Log custom trace data
if LangSmithConfig.is_configured():
    LangSmithTracer.log_trace_data(
        "my_operation",
        {
            "status": "processing",
            "items_count": 100,
            "duration_ms": 1500
        }
    )
```

## LangSmith Dashboard

### View Traces

1. Go to https://smith.langchain.com/projects
2. Select "HospitalAI" project
3. View all workflow executions and traces

### Trace Details

Each trace shows:
- **Execution time**: Duration of each step
- **Inputs/Outputs**: What was sent and received
- **Tool calls**: Which MCP tools were invoked
- **Errors**: Any exceptions or failures
- **Metadata**: Context and tags

### Example Trace Flow

```
[WORKFLOW] Issue HOSP-001 analysis
  │
  ├─ [ANALYZE STEP] (1.2s)
  │  ├─ Tool: get_issue_details("HOSP-001")
  │  ├─ Tool: get_error_logs("patient-db")
  │  ├─ Tool: get_system_metrics("patient-db-service")
  │  └─ Output: "Root cause is connection pool exhaustion"
  │
  ├─ [RESOLVE STEP] (0.8s)
  │  ├─ Tool: search_knowledge_base("connection pool")
  │  └─ Output: "2 remediation steps generated"
  │
  ├─ [VALIDATE STEP] (0.6s)
  │  ├─ Tool: get_system_metrics("patient-db-service")
  │  └─ Output: "Issue resolved = True"
  │
  └─ [ASSIGN STEP] (0.4s)
     └─ Output: "Assigned to john.smith@hospital.com"
```

## Datasets & Evaluation

### Create Evaluation Dataset

```python
from src.config.langsmith import LangSmithMonitor

# Define test cases
test_cases = [
    {
        "inputs": {
            "issue_id": "HOSP-001",
            "description": "Database timeout",
            "severity": "Critical"
        },
        "outputs": {
            "root_cause": "connection pool exhaustion",
            "is_resolved": True
        },
        "metadata": {"category": "database"}
    }
]

# Create dataset in LangSmith
dataset_id = LangSmithMonitor.create_evaluation_dataset(
    name="IssueAnalysis",
    description="Test cases for issue analysis workflow",
    examples=test_cases
)
```

### Run Evaluation

```python
# Evaluate workflow against dataset
results = evaluate(
    predict=lambda x: workflow.invoke(x),
    data=dataset_id,
    evaluators=[...]
)
```

## Monitoring & Analytics

### Monitor Traces

```python
from src.config.langsmith import LangSmithMonitor

# Get recent traces
traces = LangSmithMonitor.get_project_traces("HospitalAI")

for trace in traces:
    print(f"Trace: {trace.name}")
    print(f"Duration: {trace.end_time - trace.start_time}")
    print(f"Status: {'✓' if not trace.error else '✗'}")
```

### Common Queries

**Find slow executions:**
```
Filter: duration > 5000 (ms)
Project: HospitalAI
```

**Find errors:**
```
Filter: error is not null
Project: HospitalAI
```

**Analyze specific issue:**
```
Filter: issue_id = "HOSP-001"
Project: HospitalAI
```

## Integration Points

### 1. Workflow Tracing

All workflow steps automatically trace:
- `src/workflows/issue_workflow.py` - analyze, resolve, validate, assign steps

### 2. Logger Integration

Centralized logging works with LangSmith:
```python
logger.info("Message")  # Goes to console & file
# Also traced to LangSmith if configured
```

### 3. Agent Execution

Agent calls are traced:
```python
crew.kickoff(inputs=data)  # Traced to LangSmith
```

### 4. Tool Calls

MCP tool invocations are traced:
- `get_issue_details()`
- `get_error_logs()`
- `get_system_metrics()`
- `search_knowledge_base()`

## Best Practices

### 1. Add Context

Include relevant metadata in traces:
```python
LangSmithTracer.log_trace_data("operation", {
    "user": "john.smith@hospital.com",
    "issue_severity": "Critical",
    "environment": "production"
})
```

### 2. Handle Failures

Log errors with full context:
```python
try:
    result = agent.execute()
except Exception as e:
    LangSmithTracer.log_trace_data("error", {
        "error": str(e),
        "operation": "agent_execution",
        "fallback": "used_cached_result"
    })
```

### 3. Monitor Performance

Track execution times:
```python
start = time.time()
result = workflow.invoke(state)
duration = time.time() - start

LangSmithTracer.log_trace_data("performance", {
    "workflow_duration_ms": int(duration * 1000),
    "steps": len(state["messages"])
})
```

### 4. Tag Traces

Use metadata for filtering:
```python
LangSmithTracer.log_trace_data("event", {
    "tags": ["production", "critical", "database"],
    "correlation_id": "abc-123"
})
```

## Troubleshooting

### Traces Not Appearing

1. **Check API Key**
   ```bash
   echo $LANGSMITH_API_KEY
   ```

2. **Enable Tracing**
   ```bash
   export LANGSMITH_TRACING_V2="true"
   ```

3. **Check Configuration**
   ```python
   from src.config.langsmith import LangSmithConfig
   print(LangSmithConfig.is_configured())
   ```

### Too Many Traces

Reduce trace verbosity:
```python
# Only trace major operations
@LangSmithTracer.trace_agent_call("Agent", "Operation")
def major_operation():
    pass
```

### Performance Impact

LangSmith adds minimal overhead:
- Asynchronous tracing (non-blocking)
- Typical overhead: < 100ms per request
- Can be disabled with `LANGSMITH_TRACING_V2=false`

## Environment Configuration

### Development

```bash
export LANGSMITH_PROJECT="HospitalAI-Dev"
export LANGSMITH_TRACING_V2="true"
export LOG_LEVEL="DEBUG"
```

### Production

```bash
export LANGSMITH_PROJECT="HospitalAI-Prod"
export LANGSMITH_TRACING_V2="true"
export LOG_LEVEL="INFO"
```

### Disabled (Optional)

```bash
export LANGSMITH_TRACING_V2="false"  # Disable tracing
```

## Example Workflow with Tracing

```python
from src.workflows.issue_workflow import create_issue_workflow
from src.config.langsmith import LangSmithConfig
import json

# Setup
print("LangSmith Configuration:")
print(f"  Project: {LangSmithConfig.PROJECT}")
print(f"  Enabled: {LangSmithConfig.TRACING_ENABLED}")
print()

# Create workflow (automatically traces)
workflow = create_issue_workflow()

# Run workflow
state = workflow.invoke({
    "issue_id": "HOSP-001",
    "description": "Patient database connection timeout",
    "severity": "Critical",
    "root_cause": "",
    "analysis_confidence": 0.0,
    "remediation_steps": [],
    "is_resolved": False,
    "assigned_to": "",
    "messages": [],
    "created_at": "2026-06-06T15:00:00Z",
    "updated_at": "2026-06-06T15:00:00Z",
    "error": ""
})

# Results with tracing
print("Workflow Results:")
print(f"  Issue: {state['issue_id']}")
print(f"  Root Cause: {state['root_cause'][:100]}")
print(f"  Resolved: {state['is_resolved']}")
print(f"  Assigned To: {state['assigned_to']}")
print()
print("✅ All steps traced to LangSmith dashboard")
print("   Visit: https://smith.langchain.com/projects")
```

## Related Documentation

- [LangSmith Official Docs](https://docs.smith.langchain.com/)
- [LangSmith API Reference](https://api.smith.langchain.com/redoc)
- [Centralized Logging](CENTRALIZED_LOGGING.md)
- [Workflow Documentation](src/workflows/)

---

**Last Updated**: 2026-06-06  
**Status**: Active - LangSmith integration complete  
**Required**: LangSmith API key from https://smith.langchain.com
