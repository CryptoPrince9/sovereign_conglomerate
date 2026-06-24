import urllib.request
import json

url = "http://localhost:5000/v1/models"
print("Checking local server:", url)

try:
    with urllib.request.urlopen(url, timeout=5) as response:
        html = response.read().decode('utf-8')
        print("Success! Models:", json.loads(html))
except Exception as e:
    print("Failed to connect to local server:", e)
