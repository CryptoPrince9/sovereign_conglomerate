import sys
import os

# GEMINI_API_KEY is read from environment variable or dotenv file.

from state import ProjectState
from graph import build_graph

print("Building graph...")
try:
    workflow = build_graph()
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)

state = {
    "messages": [],
    "project_scope": {"description": "We need an AI agent to automatically format code using Black and Flake8. Output an architecture document. test_wallet_bypass"},
    "quoted_price_usdt": 0.0,
    "escrow_address": "0x11D997C9134D8c60E76AA9F3c010fe90EFA9315A",
    "payment_status": "PAID",
    "assigned_agents": ["consultant_agent"],
    "agent_outputs": {},
    "qa_status": "PENDING",
    "qa_feedback": "",
    "client_deliverable": ""
}

print("Running graph from router...")
try:
    for event in workflow.stream(state, {"recursion_limit": 100}):
        for node, state_update in event.items():
            print(f"Finished node: {node}")
            state.update(state_update)
            if state.get("qa_status") == "ERROR":
                print("QA Status ERROR hit!")
                sys.exit(1)
except Exception as e:
    import traceback
    traceback.print_exc()
