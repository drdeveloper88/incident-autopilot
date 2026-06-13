"""Resolve task - creates task for resolver agent."""

from crewai import Task
from src.agents import create_resolver_agent


def create_resolve_task() -> Task:
    """Create the resolve task."""

    return Task(
        description="Find solutions and generate remediation steps",
        expected_output="List of remediation steps",
        agent=create_resolver_agent(),
    )
