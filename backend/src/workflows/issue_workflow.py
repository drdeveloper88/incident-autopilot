"""Workflow router - returns appropriate issue-resolution workflow."""

from typing import Literal
from langgraph.graph import StateGraph

from src.config.logger import get_logger

logger = get_logger("IssueWorkflow")


def create_issue_workflow(workflow_type: Literal["sequential", "approval"] = "sequential") -> StateGraph:
    """
    Factory function returning the requested workflow type.
    
    Args:
        workflow_type: "sequential" (default) or "approval"
        
    Returns:
        Compiled LangGraph StateGraph workflow
    """
    
    if workflow_type == "approval":
        logger.info("Using approval-based workflow")
        from src.workflows.approval_based_workflow import create_approval_based_workflow
        return create_approval_based_workflow()
    else:
        logger.info("Using sequential workflow (default)")
        from src.workflows.sequential_issue_workflow import create_sequential_workflow
        return create_sequential_workflow()
