import os
import sys

# GEMINI_API_KEY is read from environment variable or dotenv file.

from state import ProjectState
from graph import build_graph

def run_tests():
    print("==================================================")
    print("TESTING NEW CAPABILITIES & SPECIALIZED AGENTS")
    print("==================================================")
    
    print("Building LangGraph workflow...")
    try:
        workflow = build_graph()
        print("Graph compiled successfully.")
    except Exception as e:
        print(f"Failed to compile graph: {e}")
        sys.exit(1)
        
    # Scope 1: Earth Science & Geology Swarms
    state_geology = {
        "messages": [],
        "project_scope": {"description": "Perform structural geology analysis and map potential rare earth metal deposits. Generate index and audio files. test_wallet_bypass"},
        "quoted_price_usdt": 0.0,
        "escrow_address": "0x11D997C9134D8c60E76AA9F3c010fe90EFA9315A",
        "payment_status": "PAID",
        "assigned_agents": [],
        "agent_outputs": {},
        "qa_status": "PENDING",
        "qa_feedback": "",
        "client_deliverable": ""
    }
    
    print("\nScope 1: Running Geology Swarm Task...")
    try:
        for event in workflow.stream(state_geology, {"recursion_limit": 100}):
            for node, state_update in event.items():
                print(f"Finished node: {node}")
                state_geology.update(state_update)
        print("Geology Swarm Task finished.")
        print(f"Assigned Agents: {state_geology.get('assigned_agents')}")
        print(f"Client Deliverable Snippet: {str(state_geology.get('client_deliverable'))[:300]}...")
    except Exception as e:
        print(f"Geology Swarm Task failed: {e}")
        
    # Scope 2: IoT Edge Healing
    state_iot = {
        "messages": [],
        "project_scope": {"description": "Perform IoT Edge server health check. The edge server at 192.168.1.50 has health metric 0.4 and workload 'payment_processor'. Run remediation. test_wallet_bypass"},
        "quoted_price_usdt": 0.0,
        "escrow_address": "0x11D997C9134D8c60E76AA9F3c010fe90EFA9315A",
        "payment_status": "PAID",
        "assigned_agents": [],
        "agent_outputs": {},
        "qa_status": "PENDING",
        "qa_feedback": "",
        "client_deliverable": ""
    }
    
    print("\nScope 2: Running IoT Edge Healing Task...")
    try:
        for event in workflow.stream(state_iot, {"recursion_limit": 100}):
            for node, state_update in event.items():
                print(f"Finished node: {node}")
                state_iot.update(state_update)
        print("IoT Edge Healing Task finished.")
        print(f"Assigned Agents: {state_iot.get('assigned_agents')}")
        print(f"Client Deliverable Snippet: {str(state_iot.get('client_deliverable'))[:300]}...")
    except Exception as e:
        print(f"IoT Edge Healing Task failed: {e}")

if __name__ == "__main__":
    run_tests()
