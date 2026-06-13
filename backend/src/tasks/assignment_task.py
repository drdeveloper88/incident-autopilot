"""Assignment task - creates task for assignment agent."""

from crewai import Task
from src.agents import create_assignment_agent


def create_assignment_task() -> Task:
    """Create the assignment task."""

    return Task(
        description="Assign the unresolved issue to an appropriate developer",
        expected_output="Developer name and contact",
        agent=create_assignment_agent(),
    )
