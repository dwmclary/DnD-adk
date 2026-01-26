
import os
from google import genai

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    models = client.models.list()
    print("Available models:")
    for m in models:
        print(f"- {m.name}")
        if "imagen" in m.name.lower():
            print(f"  (Likely Imagen match: {m.name})")
except Exception as e:
    print(f"Error listing models: {e}")
