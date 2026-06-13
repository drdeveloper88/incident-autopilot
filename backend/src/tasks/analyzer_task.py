"""Analyze task - creates task for analyzer agent."""

from crewai import Task
from src.agents import create_analyzer_agent


def create_analyze_task() -> Task:
    """Create the analyze task."""

    return Task(
        description="Analyze the issue to identify root cause",
        expected_output="Detailed root cause analysis",
        agent=create_analyzer_agent(),
    )
