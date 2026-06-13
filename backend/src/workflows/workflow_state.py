"""Type definitions for issue resolution workflow state."""

from typing import TypedDict, Optional, List, Dict, Any


class IssueState(TypedDict, total=False):
    """State for sequential issue resolution workflow."""
    
    issue_id: str
    description: str
    severity: str  # "low", "medium", "high"
    root_cause: str
    analysis_confidence: float  # 0.0 to 1.0
    remediation_steps: List[str]
    is_resolved: bool
    assigned_to: str
    messages: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    error: str
    execution_metrics: Dict[str, Dict[str, Any]]


class ExtendedIssueState(IssueState):
    """Extended state for approval-based workflow."""
    
    category: Optional[str]
    issue_type: Optional[str]
    solution_approved: bool
