import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Fetching available models...\n")

try:
    models = genai.list_models()

    for model in models:
        print(f"Model Name: {model.name}")
        print(f"Supported Methods: {model.supported_generation_methods}")
        print("-" * 50)

except Exception as e:
    print("Error:", e)