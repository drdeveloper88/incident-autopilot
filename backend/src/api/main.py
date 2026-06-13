"""FastAPI Application - REST API for Ticket Resolution AI."""

import logging
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.schemas import IssueCreate, IssueResponse
from src.workflows import create_issue_workflow

# Setup logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Ticket Resolution AI",
    description="Enterprise-grade Agentic AI system for real-time ticket analysis, resolution, and developer assignment",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow
try:
    workflow = create_issue_workflow()
    logger.info("Workflow initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize workflow: {e}")
    workflow = None

issue_store = {}  # Simple in-memory store


@app.on_event("startup")
async def startup():
    """Application startup."""
    logger.info("Ticket Resolution AI application starting...")
    logger.info(f"LLM Provider: {settings.llm_provider}")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "workflow_ready": workflow is not None,
    }


@app.post("/issues", response_model=IssueResponse)
async def create_issue(issue: IssueCreate):
    """Create and process an issue."""

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Workflow not initialized",
        )

    issue_id = issue.issue_id or str(uuid4())
    now = datetime.utcnow().isoformat()

    # Create initial state
    initial_state = {
        "issue_id": issue_id,
        "description": issue.description,
        "severity": issue.severity,
        "root_cause": "",
        "analysis_confidence": 0.0,
        "remediation_steps": [],
        "is_resolved": False,
        "assigned_to": "",
        "messages": [],
        "created_at": now,
        "updated_at": now,
        "error": "",
        "execution_metrics": {},
    }

    try:
        # Execute workflow
        logger.info(f"Invoking workflow for issue {issue_id}")
        result = workflow.invoke(initial_state)
        logger.info(f"Workflow execution completed for issue {issue_id}")

        # Store in memory
        issue_store[issue_id] = result

        return IssueResponse(**result)

    except Exception as e:
        logger.error(f"Workflow execution failed: {e}", exc_info=True)
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Full traceback: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow execution failed: {str(e)}",
        )


@app.get("/issues/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: str):
    """Retrieve issue details."""

    if issue_id not in issue_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue {issue_id} not found",
        )

    return IssueResponse(**issue_store[issue_id])
