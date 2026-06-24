import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

key = os.getenv("GEMINI_API_KEY", "dummy-key")
print("Testing key:", key[:10] + "..." if key else "None")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=key,
        temperature=0.2
    )
    res = llm.invoke([HumanMessage(content="Hello, reply with only one word 'success'.")])
    print("API Response:", res.content)
except Exception as e:
    print("API Call failed:", e)
