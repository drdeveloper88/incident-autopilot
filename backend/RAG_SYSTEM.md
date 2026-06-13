# RAG (Retrieval-Augmented Generation) System

## Overview

The RAG system uses **Chroma** vector database for semantic search over a knowledge base. It enables agents to retrieve relevant solutions, error patterns, and procedures when resolving issues.

## Architecture

### Components

1. **ChromaKnowledgeBase** (`src/tools/chroma_kb.py`)
   - Vector database client using Chroma
   - Three collections: Solutions, Error Patterns, Procedures
   - Semantic search using embeddings

2. **RAGTools** (`src/tools/rag_tools.py`)
   - CrewAI-compatible tools wrapping Chroma
   - Search methods for each collection type
   - Comprehensive search across all collections

3. **RAG Agent** (`src/agents/rag_agent.py`)
   - CrewAI agent using RAG tools
   - Specialized in knowledge base search
   - Augments issue analysis with historical data

4. **RAG Task** (`src/tasks/rag_task.py`)
   - Task definition for RAG agent
   - Orchestrates knowledge base searches

## Data Collections

### Solutions
- **Purpose**: Store known issue resolutions
- **Fields**: Title, Description, Steps, Root Cause, Tags
- **Search**: Find similar issues and their solutions

Example:
```python
kb.add_solution(
    solution_id="sol_001",
    title="Database Connection Timeout",
    description="Database connection fails with timeout error",
    steps=["Check DB status", "Verify network", "Increase timeout"],
    root_cause="Database server unreachable",
    tags=["database", "timeout", "network"]
)
```

### Error Patterns
- **Purpose**: Catalog common errors and their characteristics
- **Fields**: Error Signature, Symptoms, Resolution, Frequency
- **Search**: Find errors matching the current issue

Example:
```python
kb.add_error_pattern(
    pattern_id="pat_001",
    error_signature="Connection refused",
    symptoms="Cannot connect to service",
    resolution="Check if service is running",
    frequency="frequent"
)
```

### Procedures
- **Purpose**: Store operational procedures and best practices
- **Fields**: Title, Description, Steps, Prerequisites
- **Search**: Find relevant procedures for issue resolution

Example:
```python
kb.add_procedure(
    proc_id="proc_001",
    title="Emergency Restart",
    description="Safely restart services with minimal downtime",
    steps=["Stop services", "Clear cache", "Start services"],
    prerequisites=["SSH access", "Admin credentials"]
)
```

## Usage

### 1. Initialize Knowledge Base

```bash
python scripts/init_knowledge_base.py
```

This populates the database with sample solutions, error patterns, and procedures.

### 2. Use RAG Agent in Workflow

```python
from src.agents import create_rag_agent
from src.tasks import create_rag_task

# Create RAG agent and task
rag_agent = create_rag_agent()
rag_task = create_rag_task()

# Use in CrewAI workflow
crew = Crew(
    agents=[rag_agent, other_agents],
    tasks=[rag_task, other_tasks],
)

result = crew.kickoff(inputs={"issue_id": "JIRA-123"})
```

### 3. Direct Knowledge Base Access

```python
from src.tools.chroma_kb import ChromaKnowledgeBase

kb = ChromaKnowledgeBase()

# Search for solutions
results = kb.search_solutions("database timeout", top_k=3)

# Search for error patterns
patterns = kb.search_patterns("Connection refused", top_k=3)

# Search for procedures
procedures = kb.search_procedures("restart service", top_k=3)

# Comprehensive search
all_results = kb.search_all("OutOfMemoryError", top_k=2)
```

### 4. Add Data to Knowledge Base

```python
from src.tools.chroma_kb import ChromaKnowledgeBase

kb = ChromaKnowledgeBase()

# Add a solution
kb.add_solution(
    solution_id="sol_custom_001",
    title="Custom Issue Fix",
    description="How to fix specific custom issue",
    steps=["Step 1", "Step 2", "Step 3"],
    root_cause="Root cause explanation",
    tags=["custom", "important"]
)

# Add an error pattern
kb.add_error_pattern(
    pattern_id="pat_custom_001",
    error_signature="Custom error message",
    symptoms="What user observes",
    resolution="How to fix it",
    frequency="frequent"
)

# Add a procedure
kb.add_procedure(
    proc_id="proc_custom_001",
    title="Custom Procedure",
    description="What this procedure does",
    steps=["Step 1", "Step 2"],
    prerequisites=["Required access"]
)
```

## RAG Tools

### Available Tools

1. **search_solutions(query, top_k=3)**
   - Search for relevant solutions
   - Returns title, root cause, and resolution steps

2. **search_error_patterns(query, top_k=3)**
   - Search for matching error patterns
   - Returns error signature, symptoms, and resolution

3. **search_procedures(query, top_k=3)**
   - Search for operational procedures
   - Returns title, description, and prerequisites

4. **search_all(query, top_k=2)**
   - Comprehensive search across all collections
   - Useful for broad issue investigation

5. **get_kb_stats()**
   - Get knowledge base statistics
   - Shows number of entries in each collection

## Integration with Workflow

The RAG system can be integrated into different workflow types:

### Sequential Workflow
```python
# Sequential: analyze → rag_search → resolve → validate → assign
```

### Approval-Based Workflow
```python
# Approval: retrieval → classification → rag_search → analyze → resolve → approval → validate → assign
```

## Performance Considerations

### Embeddings
- Chroma uses default embeddings (OpenAI embeddings via langchain)
- For offline use, consider using local embeddings

### Storage
- Persistent storage in `./data/chroma_db`
- First search may be slower due to embedding generation
- Subsequent searches use cached embeddings

### Scaling
- For large datasets (>100k items), consider:
  - Partitioning by category
  - Using dedicated vector database (Pinecone, Weaviate)
  - Implementing caching layer

## Best Practices

1. **Keep Data Organized**
   - Use consistent naming conventions
   - Tag items for easy discovery
   - Group related solutions together

2. **Maintain Quality**
   - Verify solutions are accurate
   - Update procedures when processes change
   - Remove duplicate or outdated entries

3. **Regular Updates**
   - Add new solutions as issues are resolved
   - Review and update error patterns quarterly
   - Refresh procedures when systems change

4. **Monitor Performance**
   - Track search accuracy
   - Monitor query latency
   - Analyze which searches return good matches

## Troubleshooting

### No results found
- Check if knowledge base is populated
- Try simpler search queries
- Verify collection types contain relevant data

### Slow searches
- Chroma may need to generate embeddings
- Check available system memory
- Consider implementing caching

### Incorrect matches
- Refine search queries
- Review knowledge base data quality
- Adjust top_k parameter for more results

## Future Enhancements

1. **Custom Embeddings**: Use domain-specific embedding models
2. **Multi-Tenancy**: Support multiple independent knowledge bases
3. **Version Control**: Track knowledge base changes over time
4. **Feedback Loop**: Learn from agent feedback to improve matches
5. **Hybrid Search**: Combine keyword and semantic search
6. **Integration**: Connect to external knowledge bases (Confluence, Notion)
