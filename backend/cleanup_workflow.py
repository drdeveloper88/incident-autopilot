#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cleanup script to fix issue_workflow.py"""

CLEAN_CONTENT = '''"""LangGraph workflow for issue resolution with production-ready tracing and monitoring.

This module provides workflow routing to choose between two workflow types:
1. Sequential Workflow (4 steps) - analyze resolve validate assign
2. Approval-Based Workflow (7 steps) - retrieval classification analyze resolve approval validate assign
"""
from typing import Literal

from src.workflows.workflow_state import IssueState, ExtendedIssueState
from src.config.logger import get_logger

# Configure centralized logging
logger = get_logger("IssueWorkflow")

# Export states for backward compatibility
__all__ = [
    "create_issue_workflow",
    "IssueState",
    "ExtendedIssueState",
]


def create_issue_workflow(workflow_type: Literal["sequential", "approval"] = "sequential"):
    """Create and return the selected workflow type.
    
    Args:
        workflow_type: Type of workflow to create
            - "sequential": 4-step workflow
            - "approval": 7-step workflow with approval gates 
    
    Returns:
        Compiled StateGraph for issue resolution
        
    Raises:
        ValueError: If workflow_type is not recognized
    """
    # Lazy imports to avoid circular dependencies
    if workflow_type == "sequential":
        from src.workflows.sequential_issue_workflow import create_sequential_workflow
        logger.info("Creating Sequential Workflow")
        return create_sequential_workflow()
    elif workflow_type == "approval":
        from src.workflows.approval_based_workflow import create_approval_based_workflow
        logger.info("Creating Approval-Based Workflow")
        return create_approval_based_workflow()
    else:
        raise ValueError(
            f"Unknown workflow type: {workflow_type}. "
            f"Supported types: 'sequential', 'approval'"
        )
'''

filepath = r"c:\projects\dambar projects\issue-resolution-agentic-platform\src\workflows\issue_workflow.py"
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(CLEAN_CONTENT)
    
print(f"Cleaned {filepath}")

