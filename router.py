import json
from state import ProjectState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model=os.getenv("LLM_MODEL_NAME", "gemini-2.5-pro"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.0
)

AVAILABLE_AGENTS = [
    "consultant_agent", "defi_architect_agent", "regenagri_agent", 
    "edtech_agent", "macro_fiscal_agent", "b2b_automation_agent", 
    "micro_saas_agent", "community_manager_agent"
]

def router_node(state: ProjectState):
    """
    Router Agent parses the project scope and sets the 'assigned_agents' state flag.
    """
    print("[ROUTER AGENT] Parsing scope and assigning sub-agents...")
    scope_str = str(state.get("project_scope", ""))
    
    prompt = f"""
    You are the Router Agent. Based on the following project scope, determine which of the available agents are needed.
    Scope: {scope_str}
    
    Available agents: {AVAILABLE_AGENTS}
    
    Respond ONLY with a JSON array of agent names. For example: ["consultant_agent", "micro_saas_agent"]
    """
    
    try:
        response = llm.invoke([SystemMessage(content="You return only JSON arrays."), HumanMessage(content=prompt)])
        # Fallback parsing
        clean_resp = response.content.strip()
        if clean_resp.startswith("```json"):
            clean_resp = clean_resp.replace("```json", "").replace("```", "").strip()
        assigned = json.loads(clean_resp)
        # Validate against available agents
        assigned = [a for a in assigned if a in AVAILABLE_AGENTS]
    except Exception as e:
        print(f"[ROUTER AGENT] LLM fallback due to error: {e}")
        # Fallback heuristic
        assigned = []
        if "defi" in scope_str.lower(): assigned.append("defi_architect_agent")
        if "saas" in scope_str.lower(): assigned.append("micro_saas_agent")
        if not assigned: assigned.append("consultant_agent")

    state["assigned_agents"] = assigned
    print(f"[ROUTER AGENT] Assigned: {assigned}")
    return state

def route_to_specialists(state: ProjectState):
    """Conditional edge returning the list of nodes to execute in parallel."""
    return state.get("assigned_agents", [])

def check_payment_status(state: ProjectState):
    """Conditional edge to check if treasury verified payment."""
    if state.get("payment_status") == "PAID":
        return "router"
    return "wait_for_payment"

def check_qa_status(state: ProjectState):
    """Conditional edge post Executive Coach QA."""
    if state.get("qa_status") == "APPROVED":
        return "delivery"
    # If rejected, route back to all assigned agents for revision
    print(f"[SYSTEM] QA Rejected: {state.get('qa_feedback')}. Re-routing to specialists...")
    return state.get("assigned_agents", [])
