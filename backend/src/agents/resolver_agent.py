"""Resolver agent - finds solutions and remediation steps."""

from crewai import Agent
from langchain_groq import ChatGroq
from src.config.settings import settings


def create_resolver_agent() -> Agent:
    """Create the resolver agent."""

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0.3,
    )

    return Agent(
        role="Issue Resolver",
        goal="Search knowledge base and find solutions for resolved root causes",
        backstory="Expert at finding solutions and generating remediation steps",
        llm=llm,
        verbose=settings.crew_verbose,
        memory=settings.crew_memory,
    )
