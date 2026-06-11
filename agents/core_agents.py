import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from state import ProjectState
from treasury.payment_gateway import treasury

load_dotenv()

# Configure for local Odysseus by default
llm = ChatGoogleGenerativeAI(
    model=os.getenv("LLM_MODEL_NAME", "gemini-2.5-pro"),
    google_api_key=os.getenv("GEMINI_API_KEY", "missing-key-please-set"),
    temperature=0.3
)

from langgraph.prebuilt import create_react_agent
from agents.tools import execute_python_code, write_deliverable_file, zip_project_directory
from langchain_core.messages import HumanMessage

# Tools available to all agents
tools = [execute_python_code, write_deliverable_file, zip_project_directory]

def build_agent_node(agent_name: str, system_prompt: str):
    """Factory to create a standard tool-equipped agent node for LangGraph."""
    def agent_node(state: ProjectState):
        print(f"[{agent_name.upper()}] Processing task with real tools...")
        
        # We use langgraph's native create_react_agent which handles tool calls natively
        agent_executor = create_react_agent(llm, tools, state_modifier=system_prompt)
        
        try:
            scope_info = f"Project Scope: {str(state.get('project_scope', {}))}\n"
            output_info = f"Current Outputs from others: {str(state.get('agent_outputs', {}))}\n"
            task_msg = f"{scope_info}{output_info}Execute your task using the tools provided if necessary. Return your final deliverable text."
            
            result = agent_executor.invoke({"messages": [HumanMessage(content=task_msg)]})
            # The result['messages'] contains the chat history; we want the last message content
            output = result["messages"][-1].content
        except Exception as e:
            print(f"[{agent_name.upper()}] Execution Error: {e}")
            output = f"[{agent_name}] Execution failed. Error: {e}"

        if "agent_outputs" not in state or state["agent_outputs"] is None:
            state["agent_outputs"] = {}
            
        state["agent_outputs"][agent_name] = output
        return state
    
    return agent_node


# ==========================================
# Agent 1: The Ingestor (High-Ticket Closer)
# ==========================================
def closer_agent_node(state: ProjectState):
    print("[CLOSER AGENT] Ingesting lead and generating quote...")
    # Simulated intake logic
    scope_str = str(state.get("project_scope", "Generic Project"))
    
    # Simple logic to determine price
    base_price = 5000.0
    if "defi" in scope_str.lower(): base_price += 3000.0
    if "saas" in scope_str.lower(): base_price += 2000.0
    
    escrow = os.getenv("TREASURY_WALLET_ADDRESS", "0x0000")
    
    state["quoted_price_usdt"] = base_price
    state["escrow_address"] = escrow
    state["payment_status"] = "PENDING"
    
    print(f"[CLOSER AGENT] Quoted {base_price} USDT. Escrow: {escrow}")
    return state


# ==========================================
# Agents 2-9: Specialized Workers
# ==========================================
consultant_agent = build_agent_node(
    "AI Consultant",
    "Goal: Design multi-agent architectures and enterprise LLM workflows. Output architecture diagrams and strategy."
)

defi_architect_agent = build_agent_node(
    "DeFi Architect",
    "Goal: Design smart contracts, tokenomics models, and liquidity routing. Output Solidity snippets and math models."
)

regenagri_agent = build_agent_node(
    "RegenAgri Consultant",
    "Goal: Model ecological site designs, Miyawaki forests, and carbon-credit baselines."
)

edtech_agent = build_agent_node(
    "EdTech Curriculum Agent",
    "Goal: Standardize vocational training frameworks and build digital syllabi."
)

macro_fiscal_agent = build_agent_node(
    "Macro Fiscal Agent",
    "Goal: Perform sovereign debt modeling, trade flow calculations, and feasibility studies."
)

b2b_automation_agent = build_agent_node(
    "B2B Automation Agent",
    "Goal: Build custom internal tool integrations and meeting transcription pipelines."
)

micro_saas_agent = build_agent_node(
    "Micro-SaaS Dev Agent",
    "Goal: Scaffold full-stack workflows, API endpoints, and database models."
)

community_manager_agent = build_agent_node(
    "Community Manager",
    "Goal: Curate premium platform insights and automate educational content drops."
)

# ==========================================
# Agent 10: Executive Coach (The Alignment Vector)
# ==========================================
def executive_coach_node(state: ProjectState):
    print("[EXECUTIVE COACH] Performing QA on aggregated outputs...")
    outputs = state.get("agent_outputs", {})
    
    # Mock evaluation logic
    if len(outputs) == 0:
        state["qa_status"] = "REVISION_REQUESTED"
        state["qa_feedback"] = "No outputs generated. Please execute assigned agents."
    else:
        state["qa_status"] = "APPROVED"
        state["qa_feedback"] = "All SOPs met. Deliverables are aligned with organizational standards."
        
    return state
