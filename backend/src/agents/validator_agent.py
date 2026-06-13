"""Validator agent - validates resolution effectiveness."""

from crewai import Agent
from langchain_groq import ChatGroq
from src.config.settings import settings


def create_validator_agent() -> Agent:
    """Create the validator agent."""

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0.3,
    )

    return Agent(
        role="Solution Validator",
        goal="Validate that proposed solutions will resolve the issue",
        backstory="Expert at evaluating solutions and confirming effectiveness",
        llm=llm,
        verbose=settings.crew_verbose,
        memory=settings.crew_memory,
    )
