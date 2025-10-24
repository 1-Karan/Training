import os
import json
import requests
from dotenv import load_dotenv
#  Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
   raise ValueError(" OPENROUTER_API_KEY not found in .env file")
#  Function to call OpenRouter API
def openrouter_call(prompt):
   """Call mistralai/mistral-7b-instruct:free model"""
   response = requests.post(
       "https://openrouter.ai/api/v1/chat/completions",
       headers={
           "Authorization": f"Bearer {API_KEY}",
           "Content-Type": "application/json",
       },
       json={
           "model": "mistralai/mistral-7b-instruct:free",
           "messages": [{"role": "user", "content": prompt}],
       },
   )
   result = response.json()
   return result["choices"][0]["message"]["content"]
# --- CHAIN STEP 1: Get topic from user ---
topic = input("Enter a topic to summarize and generate quiz: ")
# --- CHAIN STEP 2: Generate summary ---
summary_prompt = f"Summarize the topic '{topic}' in 3-4 sentences in simple and clear language."
summary = openrouter_call(summary_prompt)
# --- CHAIN STEP 3: Generate quiz based on the summary ---
quiz_prompt = f"""
You are an expert teacher.
Based on the following summary, create **3 clear and concise quiz questions** (numbered) that test understanding of the key points.
Do not include answers.  
Summary:
{summary}
"""
quiz = openrouter_call(quiz_prompt)
# --- CHAIN STEP 4: Combine results ---
final_output = f"""--- SUMMARY ---
{summary}
--- QUIZ QUESTIONS ---
{quiz}
"""
#  Print results
print(final_output)
# --- CHAIN STEP 5: Log to file ---
os.makedirs("logs", exist_ok=True)
filename = f"logs/{topic.replace(' ', '_').lower()}_chain_log.json"
with open(filename, "w") as f:
   json.dump({"topic": topic, "summary": summary, "quiz": quiz}, f, indent=4)
print(f"\nResults logged to {filename}")