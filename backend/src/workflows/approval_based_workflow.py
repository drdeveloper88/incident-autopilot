"""Approval-based workflow: analyze → resolve → approval → validate → assign."""

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import time

from src.workflows.workflow_state import ExtendedIssueState
from src.config import settings
from src.config.logger import get_logger
from src.config.langsmith import LangSmithTracer, LangSmithConfig

logger = get_logger("ApprovalWorkflow")


def _initialize_llm():
    """Initialize LLM with fallback support (Groq → Ollama)."""
    llm = None
    
    # Try Groq first
    if settings.groq_api_key:
        try:
            llm = ChatGroq(
                model=settings.groq_model,
                api_key=settings.groq_api_key,
                temperature=0.3
            )
            logger.info(f"✓ LLM initialized with Groq: {settings.groq_model}")
            return llm
        except Exception as e:
            logger.warning(f"⚠ Failed to initialize Groq: {e}")
            if not settings.use_ollama_fallback:
                raise
    
    # Fall back to Ollama
    if settings.ollama_enabled:
        try:
            llm = Ollama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0.3
            )
            logger.info(f"✓ LLM initialized with Ollama: {settings.ollama_model}")
            return llm
        except Exception as e:
            logger.error(f"✗ Failed to initialize Ollama fallback: {e}")
            raise RuntimeError("No LLM provider available (Groq and Ollama both failed)")
    
    raise RuntimeError("No LLM provider configured")


def create_approval_based_workflow() -> StateGraph:
    """
    Build approval-based issue-resolution workflow with approval gate.
    
    Flow: analyze → resolve → approval → validate → assign
    Supports: Groq (primary) → Ollama (fallback)
    """
    
    # Initialize LLM with fallback support
    llm = _initialize_llm()

    workflow = StateGraph(ExtendedIssueState)

    def _initialize_state(state: ExtendedIssueState) -> ExtendedIssueState:
        """Ensure state has required default values."""
        if "messages" not in state or not isinstance(state.get("messages"), list):
            state["messages"] = []
        if "execution_metrics" not in state:
            state["execution_metrics"] = {}
        if "error" not in state:
            state["error"] = ""
        if "solution_approved" not in state:
            state["solution_approved"] = False
        return state

    def _update_state(state: ExtendedIssueState, step: str, duration: float, data: dict) -> None:
        """Update state with metrics and audit trail."""
        state["updated_at"] = datetime.now().isoformat()
        state["execution_metrics"][step] = {
            "duration": duration,
            "timestamp": state["updated_at"],
            "status": "success" if not data.get("error") else "failed"
        }
        state["messages"].append({
            "step": step,
            "timestamp": state["updated_at"],
            "duration_seconds": duration,
            **data
        })

    def analyze_step(state: ExtendedIssueState) -> ExtendedIssueState:
        """Analyze issue to identify root cause."""
        state = _initialize_state(state)
        step_start = time.time()
        try:
            logger.info(f"[ANALYZE] Processing {state['issue_id']}")

            if LangSmithConfig.is_configured():
                LangSmithTracer.log_trace_data(
                    "analyze_step_start",
                    {"issue_id": state["issue_id"], "severity": state["severity"]}
                )

            prompt = ChatPromptTemplate.from_template(
                """You are an expert issue analyzer. Analyze the following technical issue and provide a root cause analysis.

Issue Description: {description}
Severity: {severity}
Category: {category}

Provide a clear, concise root cause analysis in 1-2 sentences. Focus on the technical aspects."""
            )
            
            chain = prompt | llm
            response = chain.invoke({
                "description": state["description"],
                "severity": state["severity"],
                "category": state.get("category", "general")
            })
            
            state["root_cause"] = response.content.strip()
            state["analysis_confidence"] = 0.85

            logger.info(f"[ANALYZE] Root cause: {state['root_cause'][:60]}...")

            step_duration = time.time() - step_start
            _update_state(state, "analyze", step_duration, {
                "root_cause": state["root_cause"][:100],
                "confidence": state["analysis_confidence"],
            })

        except Exception as e:
            step_duration = time.time() - step_start
            error_msg = f"Analysis failed: {str(e)}"
            logger.error(f"[ANALYZE] {error_msg}", exc_info=True)
            state["error"] = error_msg
            state["root_cause"] = error_msg
            state["analysis_confidence"] = 0.0
            _update_state(state, "analyze", step_duration, {"error": error_msg})

        return state

    def resolve_step(state: ExtendedIssueState) -> ExtendedIssueState:
        """Generate remediation steps for the issue."""
        state = _initialize_state(state)
        step_start = time.time()

        try:
            logger.info(f"[RESOLVE] Processing {state['issue_id']}")

            if state.get("error"):
                return state

            if LangSmithConfig.is_configured():
                LangSmithTracer.log_trace_data(
                    "resolve_step_start",
                    {"issue_id": state["issue_id"]}
                )

            prompt = ChatPromptTemplate.from_template(
                """You are a technical support specialist. Based on the root cause analysis, provide step-by-step remediation steps.

Root Cause: {root_cause}
Issue Description: {description}
Issue Type: {issue_type}

Provide 3-5 clear, actionable remediation steps. Format each step on a new line starting with a number (1., 2., etc.)."""
            )
            
            chain = prompt | llm
            response = chain.invoke({
                "root_cause": state["root_cause"],
                "description": state["description"],
                "issue_type": state.get("issue_type", "general")
            })

            result_str = response.content.strip()
            raw_steps = result_str.split("\n")
            state["remediation_steps"] = [
                s.strip() for s in raw_steps
                if s.strip() and not s.startswith("#")
            ][:10]

            logger.info(f"[RESOLVE] Generated {len(state['remediation_steps'])} steps")

            step_duration = time.time() - step_start
            _update_state(state, "resolve", step_duration, {
                "steps_count": len(state["remediation_steps"]),
            })

        except Exception as e:
            step_duration = time.time() - step_start
            error_msg = f"Resolution failed: {str(e)}"
            logger.error(f"[RESOLVE] {error_msg}", exc_info=True)
            state["error"] = error_msg
            state["remediation_steps"] = []
            _update_state(state, "resolve", step_duration, {"error": error_msg})

        return state

    def approval_step(state: ExtendedIssueState) -> ExtendedIssueState:
        """Approval gate for solution."""
        state = _initialize_state(state)
        step_start = time.time()

        try:
            logger.info(f"[APPROVAL] Reviewing solution for {state['issue_id']}")

            state["solution_approved"] = (
                len(state.get("remediation_steps", [])) > 0
                and state.get("analysis_confidence", 0) > 0.7
            )

            logger.info(f"[APPROVAL] Solution {'approved' if state['solution_approved'] else 'rejected'}")

            step_duration = time.time() - step_start
            _update_state(state, "approval", step_duration, {
                "approved": state["solution_approved"],
            })

        except Exception as e:
            state["solution_approved"] = False
            state["error"] = str(e)

        return state

    def validate_step(state: ExtendedIssueState) -> ExtendedIssueState:
        """Validate that proposed solution will resolve the issue."""
        state = _initialize_state(state)
        step_start = time.time()

        try:
            logger.info(f"[VALIDATE] Checking {state['issue_id']}")

            if not state.get("solution_approved"):
                state["is_resolved"] = False
                return state

            steps_str = "\n".join(state.get("remediation_steps", []))
            
            prompt = ChatPromptTemplate.from_template(
                """You are a QA validator. Review the proposed solution and determine if it will likely resolve the issue.

Root Cause: {root_cause}
Remediation Steps: {steps}

Respond with ONLY "YES" or "NO" on the first line, then briefly explain your reasoning."""
            )
            
            chain = prompt | llm
            response = chain.invoke({
                "root_cause": state["root_cause"],
                "steps": steps_str
            })

            validation_text = response.content.strip().upper()
            is_valid = "YES" in validation_text
            state["is_resolved"] = is_valid and state.get("solution_approved", False)

            logger.info(f"[VALIDATE] Solution valid: {state['is_resolved']}")

            step_duration = time.time() - step_start
            _update_state(state, "validate", step_duration, {
                "is_resolved": state["is_resolved"],
                "validation_feedback": validation_text[:100],
            })

        except Exception as e:
            state["is_resolved"] = False
            state["error"] = str(e)

        return state

    def assign_step(state: ExtendedIssueState) -> ExtendedIssueState:
        """Assign unresolved issue to a developer."""
        state = _initialize_state(state)
        step_start = time.time()

        try:
            if state.get("is_resolved") or state.get("error"):
                logger.info(f"[ASSIGN] Skipped - Issue resolved or error present")
                return state

            logger.info(f"[ASSIGN] Processing {state['issue_id']}")

            if LangSmithConfig.is_configured():
                LangSmithTracer.log_trace_data(
                    "assign_step_start",
                    {"issue_id": state["issue_id"]}
                )

            prompt = ChatPromptTemplate.from_template(
                """You are a team lead assigning tickets. Based on the issue severity and description, recommend a developer to assign this ticket.

Severity: {severity}
Description: {description}
Category: {category}

Respond with ONLY the developer name (e.g., "Alice", "Bob", "Charlie") who would be best suited for this issue."""
            )
            
            chain = prompt | llm
            response = chain.invoke({
                "severity": state["severity"],
                "description": state["description"],
                "category": state.get("category", "general")
            })

            developer_name = response.content.strip()
            state["assigned_to"] = developer_name[:50]

            logger.info(f"[ASSIGN] Assigned to: {state['assigned_to']}")

            step_duration = time.time() - step_start
            _update_state(state, "assign", step_duration, {
                "assigned_to": state["assigned_to"],
            })

        except Exception as e:
            step_duration = time.time() - step_start
            error_msg = f"Assignment failed: {str(e)}"
            logger.error(f"[ASSIGN] {error_msg}", exc_info=True)
            state["error"] = error_msg
            _update_state(state, "assign", step_duration, {"error": error_msg})

        return state

    def should_assign(state: ExtendedIssueState) -> str:
        """Conditional edge: route to assign if not resolved."""
        return "assign" if not state.get("is_resolved") else END

    # Add nodes to workflow
    workflow.add_node("analyze", analyze_step)
    workflow.add_node("resolve", resolve_step)
    workflow.add_node("approval", approval_step)
    workflow.add_node("validate", validate_step)
    workflow.add_node("assign", assign_step)

    # Define edges
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "resolve")
    workflow.add_edge("resolve", "approval")
    workflow.add_edge("approval", "validate")
    workflow.add_conditional_edges("validate", should_assign, {
        "assign": "assign",
        END: END
    })
    workflow.add_edge("assign", END)

    return workflow.compile()

