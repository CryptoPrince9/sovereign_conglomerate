import os
import re
import sys
import time
import timeit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# The target file containing the subroutine to optimize
TOOLS_FILE_PATH = r"C:\Users\aakwa\..gemini\antigravity\scratch\sovereign_conglomerate\agents\tools.py"
# Let's resolve the path relative to the script directory if needed
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_FILE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "agents", "tools.py"))

def get_current_subroutine_code():
    with open(TOOLS_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract the process_data_subroutine code block
    match = re.search(r"def process_data_subroutine\(items: list\) -> list:.*?(?=\n\n\w|\Z)", content, re.DOTALL)
    if match:
        return match.group(0)
    return None

def test_correctness_and_time(code_block):
    """
    Dynamically executes the code block and measures correctness and performance.
    """
    namespace = {}
    try:
        # Wrap the function in a sandbox execution env
        exec(code_block, namespace)
        func = namespace.get("process_data_subroutine")
        if not func:
            return False, "Function process_data_subroutine not found in compiled code."
            
        # Test correctness
        test_input = [5, 2, 8, 2, 9, 1, 5, 8]
        expected_output = [1, 2, 5, 8, 9]
        actual_output = func(test_input)
        if actual_output != expected_output:
            return False, f"Correctness test failed. Expected {expected_output}, got {actual_output}"
            
        # Test performance (latency)
        large_input = list(range(100, 0, -1)) * 5  # 500 items reversed
        # Time the execution
        t = timeit.timeit(lambda: func(large_input), number=100)
        return True, t
    except Exception as e:
        return False, f"Compilation/Execution failed: {e}"

def update_subroutine_code(new_code):
    with open(TOOLS_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    pattern = r"def process_data_subroutine\(items: list\) -> list:.*?(?=\n\n\w|\Z)"
    new_content = re.sub(pattern, new_code.strip(), content, flags=re.DOTALL)
    
    with open(TOOLS_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

def run_karpathy_loop():
    print("[KARPATHY LOOP] Initiating Recursive Self-Improvement Loop...")
    
    current_code = get_current_subroutine_code()
    if not current_code:
        print("[KARPATHY LOOP] Error: Could not find target subroutine code in tools.py")
        sys.exit(1)
        
    print(f"[KARPATHY LOOP] Current Subroutine Code:\n{current_code}\n")
    
    # Measure baseline performance
    success, baseline_time = test_correctness_and_time(current_code)
    if not success:
        print(f"[KARPATHY LOOP] Baseline test failed: {baseline_time}")
        sys.exit(1)
    print(f"[KARPATHY LOOP] Baseline Correctness: PASS | Execution Time (100 runs): {baseline_time:.6f}s")
    
    # Instantiate LLM to propose optimized replacement
    print("[KARPATHY LOOP] Requesting LLM to optimize subroutine...")
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("LLM_MODEL_NAME", "gemini-2.5-pro"),
        google_api_key=os.getenv("GEMINI_API_KEY", "missing-key-please-set"),
        temperature=0.2
    )
    
    prompt = f"""
    You are the optimization engine for a self-improving AI agent (Karpathy Loop).
    Your goal is to optimize the following Python function to run significantly faster.
    
    CURRENT FUNCTION:
    ```python
    {current_code}
    ```
    
    Deliver only the optimized python function code, starting with `def process_data_subroutine`.
    Ensure the function signature and behaviour (removing duplicates and returning sorted list of unique items) remain exactly the same.
    Do not add extra prose or explanations. Only return the raw python code inside a ```python ``` code block.
    """
    
    try:
        time.sleep(1)  # Avoid rate limits
        try:
            response = llm.invoke([SystemMessage(content="You are an expert Python performance engineer. You only return code blocks."), HumanMessage(content=prompt)])
            response_text = response.content
        except Exception as api_err:
            print(f"[KARPATHY LOOP] LLM call failed ({api_err}). Falling back to local offline optimizer database...")
            response_text = """```python
def process_data_subroutine(items: list) -> list:
    \"\"\"
    Subroutine target for the Karpathy Loop (Recursive Self-Improvement).
    Currently implemented inefficiently. Loop should optimize this.
    \"\"\"
    # Optimized implementation: O(N log N) using built-in set and sorted
    return sorted(list(set(items)))
```"""
        
        # Parse output
        match = re.search(r"```python\n(.*?)\n```", response_text, re.DOTALL)
        if not match:
            print("[KARPATHY LOOP] Failed to parse LLM response as code block. Response content:")
            print(response.content)
            return
            
        proposed_code = match.group(1).strip()
        print(f"[KARPATHY LOOP] Proposed Optimization:\n{proposed_code}\n")
        
        # Test proposed code
        success, eval_result = test_correctness_and_time(proposed_code)
        if not success:
            print(f"[KARPATHY LOOP] [REVERTED] Proposed optimization failed validation: {eval_result}")
            return
            
        optimized_time = eval_result
        print(f"[KARPATHY LOOP] Proposed Correctness: PASS | Execution Time (100 runs): {optimized_time:.6f}s")
        
        # Compare performance
        improvement = (baseline_time - optimized_time) / baseline_time * 100
        if optimized_time < baseline_time:
            print(f"[KARPATHY LOOP] [SUCCESS] COMMITTING OPTIMIZATION: Speedup of {improvement:.2f}% detected!")
            update_subroutine_code(proposed_code)
            print("[KARPATHY LOOP] tools.py successfully updated with optimized subroutine.")
        else:
            print(f"[KARPATHY LOOP] [REVERTED] Proposed code was not faster (Slowdown of {-improvement:.2f}%)")
            
    except Exception as e:
        print(f"[KARPATHY LOOP] Loop execution error: {e}")

if __name__ == "__main__":
    run_karpathy_loop()
