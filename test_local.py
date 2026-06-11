import sys
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyARm8cYTv7BoM3P1ERv9BGjsFnOVyhUn8k"

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
    "project_scope": {"description": "Test local."},
    "quoted_price_usdt": 0.0,
    "escrow_address": "0x11D997C9134D8c60E76AA9F3c010fe90EFA9315A",
    "payment_status": "PAID",
    "assigned_agents": ["consultant_agent", "micro_saas_agent"],
    "agent_outputs": {},
    "qa_status": "PENDING",
    "qa_feedback": "",
    "client_deliverable": ""
}

print("Running graph...")
try:
    # Set the entry point to router to skip intake and payment which reset states
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
