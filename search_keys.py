import os

print("Searching for GEMINI_API_KEY or AIzaSy in config files...")

folders_to_search = [
    r"C:\Users\aakwa\.gemini",
    r"C:\Users\aakwa\.agents"
]

for folder in folders_to_search:
    if not os.path.exists(folder):
        continue
    for root, dirs, files in os.walk(folder):
        # skip large directories like .git or .venv
        if any(x in root for x in [".venv", ".git", "__pycache__", "node_modules", ".system_generated"]):
            continue
        for file in files:
            if file.endswith((".py", ".env", ".json", ".txt", ".md", ".sh", ".ps1")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "AIzaSy" in content or "GEMINI_API_KEY" in content:
                            print(f"Found in file: {filepath}")
                            # print lines containing the match
                            for line in content.splitlines():
                                if "AIzaSy" in line or "GEMINI_API_KEY" in line:
                                    print("  ", line[:150])
                except Exception as e:
                    pass
