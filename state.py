import operator
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage

class ProjectState(TypedDict):
    """
    The shared state for The Sovereign Conglomerate LangGraph machine.
    """
    # LangGraph standard message passing
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Intake & Treasury
    project_scope: Dict[str, Any]
    quoted_price_usdt: float
    escrow_address: Optional[str]
    payment_status: str  # e.g., "PENDING", "PAID", "RELEASED"
    
    # Routing & Execution
    assigned_agents: List[str]
    agent_outputs: Dict[str, str]
    
    # Assembly & QA
    qa_status: str  # e.g., "PENDING", "REVISION_REQUESTED", "APPROVED"
    qa_feedback: str
    
    # Delivery
    client_deliverable: str
