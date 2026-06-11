from langgraph.graph import StateGraph, END
from state import ProjectState
from agents.core_agents import (
    closer_agent_node, consultant_agent, defi_architect_agent, regenagri_agent,
    edtech_agent, macro_fiscal_agent, b2b_automation_agent, micro_saas_agent,
    community_manager_agent, executive_coach_node
)
from router import router_node, route_to_specialists, check_payment_status, check_qa_status
from treasury.payment_gateway import treasury
from memory.long_term import memory_bank

def treasury_validation_node(state: ProjectState):
    if state.get('payment_status') == 'PAID':
        return state
    """Wait for Web3 Treasury Layer to confirm USDT payment."""
    # Uses the shared treasury instance to verify funds based on the state quote
    is_paid = treasury.verify_payment(expected_amount_usdt=state.get("quoted_price_usdt", 0))
    if is_paid:
        state["payment_status"] = "PAID"
    return state

def delivery_node(state: ProjectState):
    """Final delivery by Closer and storing to long-term memory."""
    print("[CLOSER AGENT] Finalizing delivery and signaling treasury to release funds...")
    if "client_deliverable" not in state or not state["client_deliverable"]:
        state["client_deliverable"] = f"Final Agency Output:\n{str(state.get('agent_outputs'))}"
    
    # Store to long-term memory
    memory_bank.store_project(
        project_id=str(hash(str(state.get('project_scope')))), 
        scope=str(state.get('project_scope')), 
        deliverable=state["client_deliverable"]
    )
    return state

def build_graph():
    workflow = StateGraph(ProjectState)

    # 1. Add all nodes
    workflow.add_node("intake", closer_agent_node)
    workflow.add_node("wait_for_payment", treasury_validation_node)
    workflow.add_node("router", router_node)
    
    # Add the 8 specialists
    workflow.add_node("consultant_agent", consultant_agent)
    workflow.add_node("defi_architect_agent", defi_architect_agent)
    workflow.add_node("regenagri_agent", regenagri_agent)
    workflow.add_node("edtech_agent", edtech_agent)
    workflow.add_node("macro_fiscal_agent", macro_fiscal_agent)
    workflow.add_node("b2b_automation_agent", b2b_automation_agent)
    workflow.add_node("micro_saas_agent", micro_saas_agent)
    workflow.add_node("community_manager_agent", community_manager_agent)
    
    workflow.add_node("executive_coach", executive_coach_node)
    workflow.add_node("delivery", delivery_node)

    # 2. Define Edges
    workflow.set_entry_point("intake")
    workflow.add_edge("intake", "wait_for_payment")
    
    # Conditional edge from payment to router or loop back to payment
    workflow.add_conditional_edges(
        "wait_for_payment",
        check_payment_status,
        {
            "router": "router",
            "wait_for_payment": "wait_for_payment"
        }
    )

    # Conditional edge from router to the assigned specialists (parallel mapping)
    specialist_nodes = [
        "consultant_agent", "defi_architect_agent", "regenagri_agent", 
        "edtech_agent", "macro_fiscal_agent", "b2b_automation_agent", 
        "micro_saas_agent", "community_manager_agent"
    ]
    
    workflow.add_conditional_edges(
        "router",
        route_to_specialists,
        {node: node for node in specialist_nodes}
    )

    # Edges from all specialists converge to the executive coach
    for node in specialist_nodes:
        workflow.add_edge(node, "executive_coach")

    # Conditional edge from executive coach based on QA status
    workflow.add_conditional_edges(
        "executive_coach",
        check_qa_status,
        {
            "delivery": "delivery",
            **{node: node for node in specialist_nodes} # If rejected, back to assigned agents
        }
    )

    workflow.add_edge("delivery", END)

    return workflow.compile()
