import sys
from graph import build_graph

def run_agency():
    print("==================================================")
    print("🏛️ Welcome to The Sovereign Agency")
    print("==================================================")
    
    app = build_graph()
    
    scope = input("\nEnter the project scope or client request:\n> ")
    
    if not scope.strip():
        scope = "Build a DeFi tokenomics model with an integrated Micro-SaaS analytics dashboard."
        print(f"No scope provided. Defaulting to: {scope}")
    
    # Initialize the ProjectState
    initial_state = {
        "messages": [],
        "project_scope": {"description": scope},
        "quoted_price_usdt": 0.0,
        "escrow_address": None,
        "payment_status": "PENDING",
        "assigned_agents": [],
        "agent_outputs": {},
        "qa_status": "PENDING",
        "qa_feedback": "",
        "client_deliverable": ""
    }

    print("\n🚀 Commencing Framework Execution...\n")
    
    # Run the State Graph Machine
    for event in app.stream(initial_state):
        for node, state_update in event.items():
            print(f"\n--- Output from {node} ---")
            
            if "quoted_price_usdt" in state_update and state_update["quoted_price_usdt"] > 0:
                print(f"💰 Quote Generated: {state_update['quoted_price_usdt']} USDT")
                
            if "assigned_agents" in state_update and len(state_update["assigned_agents"]) > 0:
                print(f"🔗 Sub-agents Dispatched: {state_update['assigned_agents']}")
                
            if "client_deliverable" in state_update and state_update["client_deliverable"]:
                print("\n📦 FINAL DELIVERABLE PREPARED:\n")
                print(state_update["client_deliverable"])

    print("\n✅ Sovereign Agency Workflow Completed.")

if __name__ == "__main__":
    run_agency()
