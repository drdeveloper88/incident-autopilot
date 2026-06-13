# Centralized Logger Configuration

## Overview

HospitalAI now uses a **centralized logging system** for consistency, maintainability, and real-time monitoring. All modules should use the centralized logger configuration from `src/config/logger.py` instead of creating their own loggers.

## Benefits

✅ **Consistency**: All modules use the same logging format and level  
✅ **Real-time Data**: Logs are written to both console and file in real-time  
✅ **Easy Configuration**: Single point to manage log levels and outputs  
✅ **Centralization**: Similar to how data is centralized in `/data` folder  
✅ **Production-Ready**: Professional logging for monitoring and debugging  

## Architecture

```
src/
├── config/
│   └── logger.py          # Centralized logger configuration
├── tools/
│   ├── analyzer_tools.py  # Uses get_logger("AnalyzerTools")
│   ├── resolver_tools.py  # Uses get_logger("ResolverTools")
│   ├── validator_tools.py # Uses get_logger("ValidatorTools")
│   ├── mcp_server.py      # Uses get_logger("MCPServer")
│   └── langchain_mcp_adapter.py
├── agents/
├── tasks/
└── workflows/

logs/
└── hospitalai.log         # Centralized log file
```

## Usage

### Basic Usage

```python
from src.config.logger import get_logger

logger = get_logger("ModuleName")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
```

### In Different Modules

**analyzer_tools.py:**
```python
from src.config.logger import get_logger

logger = get_logger("AnalyzerTools")

def get_issue_details(issue_id):
    logger.info(f"Fetching issue: {issue_id}")
    # ... implementation
```

**resolver_tools.py:**
```python
from src.config.logger import get_logger

logger = get_logger("ResolverTools")

def search_knowledge_base(query):
    logger.info(f"Searching KB for: {query}")
    # ... implementation
```

## Configuration

### Log Level Control

Set via environment variable:

```bash
# Development (verbose)
export LOG_LEVEL=DEBUG

# Production (concise)
export LOG_LEVEL=INFO

# Default is INFO
```

### Log Output

Logs are written to:
- **Console (stderr)**: Immediate feedback during development
- **File**: `logs/hospitalai.log` for persistent record

### Log Format

```
[2026-06-06 15:30:45,123] INFO - AnalyzerTools - Fetching Jira issue: HOSP-001
[2026-06-06 15:30:46,456] INFO - ResolverTools - Found 2 knowledge base articles
[2026-06-06 15:30:47,789] ERROR - ValidatorTools - Failed to fetch metrics
```

## Factory Pattern

For more advanced use cases, use the `LoggerFactory`:

```python
from src.config.logger import LoggerFactory

# Get or create logger (cached)
logger = LoggerFactory.get_logger("MyModule")

# Reset all loggers (useful for testing)
LoggerFactory.reset_all()
```

## Real-Time Data Integration

The centralized logger works alongside centralized real-time data:

```python
from src.config.logger import get_logger
from src.tools.analyzer_tools import AnalyzerTools

logger = get_logger("Workflow")

analyzer = AnalyzerTools()

# Logs show real-time data loading
issue = analyzer.get_issue_details("HOSP-001")
# Console output:
# [2026-06-06 15:30:45,123] INFO - AnalyzerTools - Fetching Jira issue: HOSP-001
# [2026-06-06 15:30:45,234] INFO - AnalyzerTools - Found issue: HOSP-001
```

## Migration Guide

### Old Way (Deprecated)
```python
import logging

logger = logging.getLogger("MyModule")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
# ... setup formatter, add handler
```

### New Way (Recommended)
```python
from src.config.logger import get_logger

logger = get_logger("MyModule")
```

## Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed information for debugging |
| INFO | General informational messages |
| WARNING | Warning messages for potential issues |
| ERROR | Error messages for failed operations |
| CRITICAL | Critical errors requiring immediate attention |

## File Management

Logs are stored in `logs/` directory:

```bash
# View recent logs
tail -f logs/hospitalai.log

# View last 100 lines
tail -100 logs/hospitalai.log

# Search for errors
grep ERROR logs/hospitalai.log

# Search for specific module
grep AnalyzerTools logs/hospitalai.log
```

## Integration with Workflow

The centralized logger works seamlessly with the issue resolution workflow:

```python
from src.config.logger import get_logger
from src.workflows.issue_workflow import create_issue_workflow

logger = get_logger("MainWorkflow")

workflow = create_issue_workflow()

# All steps log their actions
# - analyze_step logs: "Analyzing issue..."
# - resolve_step logs: "Generating solutions..."
# - validate_step logs: "Validating fix..."
# - assign_step logs: "Assigning developer..."
```

## Best Practices

1. **Use Descriptive Module Names**: `get_logger("AnalyzerTools")` not `get_logger("tools")`
2. **Log at Appropriate Levels**:
   - INFO: Major operations (issue retrieval, data loading)
   - WARNING: Fallbacks, retries
   - ERROR: Failures with exception info
3. **Include Context**: Log with parameters for better debugging
4. **Avoid Sensitive Data**: Don't log passwords, API keys, etc.

## Example: Real-Time Data with Centralized Logging

```python
from src.config.logger import get_logger
from src.tools.analyzer_tools import AnalyzerTools

logger = get_logger("IssueAnalysis")

def analyze_issue(issue_id):
    logger.info(f"Starting analysis for issue: {issue_id}")
    
    analyzer = AnalyzerTools()
    
    try:
        # Real-time data loading with logging
        issue = analyzer.get_issue_details(issue_id)
        logger.info(f"Retrieved issue: {issue.get('summary')}")
        
        logs = analyzer.get_error_logs(issue_id)
        logger.info(f"Found {len(logs)} error logs")
        
        metrics = analyzer.get_system_metrics("patient-db-service")
        logger.info(f"System status: {metrics.get('health_status')}")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise
    
    logger.info("Analysis completed successfully")
    return {
        "issue": issue,
        "logs": logs,
        "metrics": metrics
    }
```

## Troubleshooting

### Logs not appearing
1. Check `LOG_LEVEL` environment variable
2. Verify `logs/` directory exists
3. Ensure write permissions

### Too many log messages
1. Increase `LOG_LEVEL` to WARNING or ERROR
2. Use module-specific filtering
3. Check for duplicate handlers

### File not created
1. Verify parent directory exists: `os/hospitalai.log`
2. Check filesystem permissions
3. Use DEBUG level to see setup messages

## Configuration Reference

```python
# From src/config/logger.py

class LoggerConfig:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "hospitalai.log")
```

---

**Last Updated**: 2026-06-06  
**Status**: Active - All modules migrated to centralized logging  
**Related Files**: 
- `src/config/logger.py` - Main configuration
- `src/tools/analyzer_tools.py` - Example implementation
- `src/tools/resolver_tools.py` - Example implementation
- `src/tools/validator_tools.py` - Example implementation
