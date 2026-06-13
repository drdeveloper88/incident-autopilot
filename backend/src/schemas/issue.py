"""Data schemas for API and workflows."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class IssueCreate(BaseModel):
    """Schema for creating an issue."""

    description: str = Field(..., description="Problem description")
    severity: str = Field(default="medium", description="Severity level: low/medium/high/critical")
    issue_id: Optional[str] = Field(default=None, description="Unique issue identifier")


class IssueResponse(BaseModel):
    """Schema for issue response."""

    issue_id: str
    description: str
    severity: str
    root_cause: Optional[str] = None
    analysis_confidence: float = 0.0
    remediation_steps: List[str] = []
    is_resolved: bool = False
    assigned_to: Optional[str] = None
    messages: List[Dict[str, Any]] = []
    execution_metrics: Dict[str, Any] = {}
    created_at: str
    updated_at: str
    error: Optional[str] = None
