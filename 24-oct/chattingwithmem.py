import os
import requests
from dotenv import load_dotenv
# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
   raise ValueError("OPENROUTER_API_KEY not found in .env file")
URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
   "Authorization": f"Bearer {API_KEY}",
   "Content-Type": "application/json"
}
# Chat memory
chat_memory = [
   {"role": "system", "content": "You are a helpful assistant."}
]
def chat_with_memory(user_input):
   # Append user input to memory
   chat_memory.append({"role": "user", "content": user_input})
   payload = {
       "model": "mistralai/mistral-7b-instruct:free",
       "messages": chat_memory,
       "max_tokens": 300,
       "temperature": 0.7
   }
   response = requests.post(URL, headers=HEADERS, json=payload)
   if response.status_code == 200:
       result = response.json()
       assistant_reply = result['choices'][0]['message']['content']
       # Append assistant reply to memory
       chat_memory.append({"role": "assistant", "content": assistant_reply})
       return assistant_reply
   else:
       return f"Error {response.status_code}: {response.text}"
# Chat loop
print("=== Start Chatting with Memory ===\nType 'exit' to stop.")
while True:
   user_input = input("You: ")
   if user_input.lower() == "exit":
       print("Conversation ended.")
       break
   reply = chat_with_memory(user_input)
   print("Assistant:", reply)