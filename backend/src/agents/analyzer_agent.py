"""Analyzer agent - analyzes issues to find root causes."""

from crewai import Agent
from langchain_groq import ChatGroq
from src.config.settings import settings


def create_analyzer_agent() -> Agent:
    """Create the analyzer agent."""

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0.3,
    )

    return Agent(
        role="Issue Analyzer",
        goal="Analyze issues to find root causes using available data sources",
        backstory="Expert at analyzing system issues and identifying root causes",
        llm=llm,
        verbose=settings.crew_verbose,
        memory=settings.crew_memory,
    )
