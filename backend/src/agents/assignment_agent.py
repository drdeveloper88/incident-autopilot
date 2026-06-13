"""Assignment agent - assigns unresolved issues to developers."""

from crewai import Agent
from langchain_groq import ChatGroq
from src.config.settings import settings


def create_assignment_agent() -> Agent:
    """Create the assignment agent."""

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0.3,
    )

    return Agent(
        role="Issue Assigner",
        goal="Assign unresolved issues to appropriate developers",
        backstory="Expert at matching issues with the right development team",
        llm=llm,
        verbose=settings.crew_verbose,
        memory=settings.crew_memory,
    )
