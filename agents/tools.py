import os
import zipfile
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

@tool
def execute_python_code(code: str) -> str:
    """
    Executes Python code in a REPL and returns the stdout/stderr.
    Useful for Macro Fiscal, Consultant, and DeFi agents to run math or simulations.
    """
    try:
        repl = PythonREPL()
        result = repl.run(code)
        return result
    except Exception as e:
        return f"Execution Error: {e}"

@tool
def write_deliverable_file(filename: str, content: str) -> str:
    """
    Writes a raw string to a physical file on disk in the deliverables/ directory.
    Useful for scaffolding apps or creating Markdown/PDFs.
    """
    os.makedirs("deliverables", exist_ok=True)
    filepath = os.path.join("deliverables", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File successfully written to {filepath}"

@tool
def zip_project_directory(directory_name: str) -> str:
    """
    Zips a generated directory into an archive for client delivery.
    """
    os.makedirs("deliverables", exist_ok=True)
    target_dir = os.path.join("deliverables", directory_name)
    zip_path = f"{target_dir}.zip"
    
    if not os.path.exists(target_dir):
        return f"Error: Directory {target_dir} does not exist."
        
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                zipf.write(os.path.join(root, file), 
                         os.path.relpath(os.path.join(root, file), 
                         os.path.join(target_dir, '..')))
    return f"Directory zipped successfully to {zip_path}"
