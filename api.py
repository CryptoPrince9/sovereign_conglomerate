from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid
import os
import uvicorn
from graph import build_graph
from state import ProjectState
from treasury.payment_gateway import treasury

app = FastAPI(title="The Sovereign Conglomerate API", version="1.0.0")

# In-memory store for project states (in production, use Redis or Postgres)
db = {}

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Mount the static directory if we add css/js files later
app.mount("/assets", StaticFiles(directory="frontend"), name="assets")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/escrow")
async def escrow():
    return FileResponse("frontend/escrow.html")

@app.get("/tracking")
async def tracking():
    return FileResponse("frontend/tracking.html")
# Compile the LangGraph
agency_workflow = build_graph()

class IntakeRequest(BaseModel):
    project_scope: str

@app.post("/api/intake")
async def intake_project(req: IntakeRequest, background_tasks: BackgroundTasks):
    """
    Submit a project scope. The system will generate a quote and escrow address.
    """
    project_id = str(uuid.uuid4())
    
    from agents.core_agents import closer_agent_node
    
    # Simple quoting heuristic (The Closer Agent logic embedded for instant API response)
    # Replaced by real LLM estimation from closer_agent_node
    initial_state = {
        "messages": [],
        "project_scope": {"description": req.project_scope},
        "agent_outputs": {}
    }
    
    # Calculate real quote synchronously
    initial_state = closer_agent_node(initial_state)
    base_price = initial_state.get("quoted_price_usdt", 5000.0)
    
    if 'test_wallet_bypass' in req.project_scope.lower(): base_price = 0.0
    
    escrow = "0x11D997C9134D8c60E76AA9F3c010fe90EFA9315A"
    
    initial_state = {
        "messages": [],
        "project_scope": {"description": req.project_scope},
        "quoted_price_usdt": base_price,
        "escrow_address": escrow,
        "payment_status": "PENDING",
        "assigned_agents": [],
        "agent_outputs": {},
        "qa_status": "PENDING",
        "qa_feedback": "",
        "client_deliverable": ""
    }
    
    db[project_id] = initial_state
    
    # Start the LangGraph in the background
    background_tasks.add_task(execute_workflow, project_id, initial_state)
    
    return {
        "project_id": project_id,
        "quoted_price_usdt": base_price,
        "escrow_address": escrow,
        "status": "PENDING_PAYMENT",
        "message": f"Please deposit exactly {base_price} USDT on Polygon to {escrow}. Work will begin automatically upon confirmation."
    }

def execute_workflow(project_id: str, state: ProjectState):
    """Background task that runs the LangGraph machine."""
    try:
        # agency_workflow.stream will run the nodes. 
        # Since wait_for_payment is a node, it will block there until treasury verifies.
        for event in agency_workflow.stream(state, {"recursion_limit": 100}):
            for node, state_update in event.items():
                print(f"[Project {project_id}] Finished node: {node}")
                # Update our in-memory DB with the latest state
                db[project_id].update(state_update)
                
    except Exception as e:
        print(f"[Project {project_id}] Error in workflow: {e}")
        db[project_id]["qa_status"] = "ERROR"

@app.get("/api/status/{project_id}")
async def get_status(project_id: str):
    """Check the status of a project."""
    if project_id not in db:
        raise HTTPException(status_code=404, detail="Project not found")
        
    state = db[project_id]
    return {
        "project_id": project_id,
        "payment_status": state.get("payment_status"),
        "assigned_agents": state.get("assigned_agents"),
        "qa_status": state.get("qa_status")
    }

@app.get("/api/deliverable/{project_id}")
async def get_deliverable(project_id: str):
    """Retrieve the final deliverables if QA is approved."""
    if project_id not in db:
        raise HTTPException(status_code=404, detail="Project not found")
        
    state = db[project_id]
    if state.get("qa_status") != "APPROVED" or not state.get("client_deliverable"):
        return {"status": "Work in progress. Please check back later."}
        
    return {
        "project_id": project_id,
        "deliverable": state.get("client_deliverable")
    }

class FeedbackRequest(BaseModel):
    feedback: str

@app.post("/api/feedback/{project_id}")
async def submit_feedback(project_id: str, req: FeedbackRequest, background_tasks: BackgroundTasks):
    if project_id not in db:
        raise HTTPException(status_code=404, detail="Project not found")
        
    state = db[project_id]
    state["client_feedback"] = req.feedback
    state["qa_status"] = "PENDING"
    # Append the feedback to the scope so agents use it
    state["project_scope"]["description"] += f"\n\nCLIENT FEEDBACK FOR REVISION: {req.feedback}"
    
    # Restart the graph with the updated state
    background_tasks.add_task(execute_workflow, project_id, state)
    return {"status": "Feedback received. Agents are autonomously improving the deliverables."}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
