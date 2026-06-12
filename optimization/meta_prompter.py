import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

def run_meta_prompter():
    print("[META-PROMPTER] Waking up to analyze agency failures...")
    
    error_log_path = "optimization/error_logs.txt"
    if not os.path.exists(error_log_path):
        print("[META-PROMPTER] No errors found. The agency is operating flawlessly.")
        return

    with open(error_log_path, "r", encoding="utf-8") as f:
        errors = f.read()
        
    if not errors.strip():
        print("[META-PROMPTER] Error log is empty.")
        return

    print("[META-PROMPTER] Found failure logs. Analyzing root causes...")
    
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("LLM_MODEL_NAME", "gemini-2.5-pro"),
        google_api_key=os.getenv("GEMINI_API_KEY", "missing-key-please-set"),
        temperature=0.2,
        max_retries=5
    )
    
    prompt = f"""
    You are the Sovereign Agency's Optimization Core (Meta-Prompter).
    Your goal is to read the following execution failures and tracebacks produced by the agency's specialized agents.
    
    FAILURES:
    {errors}
    
    Analyze what went wrong. Then, write a set of new, optimized System Prompt instructions that should be given to the agents to prevent them from ever making these specific coding mistakes again. Be highly specific and technical.
    """
    
    try:
        print("[META-PROMPTER] Generating optimized prompts (this may take a moment)...")
        time.sleep(10) # Respect rate limits
        result = llm.invoke([SystemMessage(content="You are a senior AI engineer optimizing LangChain agent prompts."), HumanMessage(content=prompt)])
        
        output_path = "optimization/optimized_prompts.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Autonomous Prompt Upgrades\n\n")
            f.write(result.content)
            
        print(f"[META-PROMPTER] Optimization complete. New instructions written to {output_path}")
        
        # Clear the error log after processing
        open(error_log_path, "w").close()
        print("[META-PROMPTER] Cleared error logs.")
        
    except Exception as e:
        print(f"[META-PROMPTER] Failed to generate optimizations: {e}")

if __name__ == "__main__":
    run_meta_prompter()
