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

@app.get("/")
async def root():
    return {
        "message": "Welcome to The Sovereign Conglomerate API",
        "docs": "Append /docs to the URL to view the Swagger UI documentation",
        "status": "online"
    }

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
    
    # Simple quoting heuristic (The Closer Agent logic embedded for instant API response)
    base_price = 5000.0
    if "defi" in req.project_scope.lower(): base_price += 3000.0
    if "saas" in req.project_scope.lower(): base_price += 2000.0
    
    escrow = os.getenv("TREASURY_WALLET_ADDRESS", "0x0000000000000000000000000000000000000000")
    
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

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
