import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key[:5]}...{api_key[-5:]}")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    chat = model.start_chat(history=[])
    response = chat.send_message("Hi")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")
