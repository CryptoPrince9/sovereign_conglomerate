import os
print("GEMINI_API_KEY in env:", "GEMINI_API_KEY" in os.environ)
if "GEMINI_API_KEY" in os.environ:
    print("Value starts with:", os.environ["GEMINI_API_KEY"][:10])
