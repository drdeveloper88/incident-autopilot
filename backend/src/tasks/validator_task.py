"""Validate task - creates task for validator agent."""

from crewai import Task
from src.agents import create_validator_agent


def create_validate_task() -> Task:
    """Create the validate task."""

    return Task(
        description="Validate that the proposed solution will resolve the issue",
        expected_output="Validation result",
        agent=create_validator_agent(),
    )
