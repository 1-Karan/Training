from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# Mistral model configuration
llm_config = {
    "model": "mistralai/mistral-7b-instruct:free",  # Mistral model
    "api_key": api_key,
    "base_url": base_url,
    "temperature": 0.7,
    "max_tokens": 700,
}


# Research Agent to gather detailed information
def research_agent(topic: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Research prompt for the model
    research_prompt = {
        "model": llm_config["model"],
        "messages": [
            {"role": "user", "content": f"Research the topic: {topic} and provide 10 key insights."}
        ],
        "temperature": llm_config["temperature"],
        "max_tokens": llm_config["max_tokens"],
    }

    response = requests.post(f"{base_url}/chat/completions", json=research_prompt, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        print("Error during research:", response.status_code, response.text)
        return None


# Summarizer Agent to condense the information
def summarizer_agent(research_data: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Summarize prompt for the model
    summarizer_prompt = {
        "model": llm_config["model"],
        "messages": [
            {"role": "user",
             "content": f"Summarize the following research into a short summary and 5 key bullet points:\n{research_data}"}
        ],
        "temperature": llm_config["temperature"],
        "max_tokens": 500,
    }

    response = requests.post(f"{base_url}/chat/completions", json=summarizer_prompt, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        print("Error during summarization:", response.status_code, response.text)
        return None


# Notifier function to log summary into a file
def notifier_agent(summary: str, filename: str = "summary_log.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - AUTOGEN: Notified and saved to {filename}\n")
        f.write(f"{summary}\n\n")

    print("Summary has been logged.")
    return {}


# Complete research pipeline: research -> summarize -> notify
def run_pipeline(topic: str):
    print(f"Researching the topic: '{topic}'...")
    research = research_agent(topic)

    if not research:
        print("Agent: Research failed.")
        return

    print(f"Research data: {research[:300]}...")  # Display a part of the research data
    print("\nSummarizing the research...")
    summary = summarizer_agent(research)

    if not summary:
        print("Agent: Summary generation failed.")
        return

    print(f"Summary: {summary}")
    notifier_agent(summary)


# Main Loop for user interaction
if __name__ == "__main__":
    print("\n=== Start chatting with your Agent ===")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("\nConversation ended.")
            break

        if user_input.lower().startswith("research"):
            topic = user_input.replace("research", "").strip()
            if not topic:
                print("Agent: Please specify a topic.")
                continue
            try:
                run_pipeline(topic)
            except Exception as e:
                print("Agent: Error during research flow:", e)
            continue

        else:
            print("Agent: I can help with research. Type 'research <your topic>' to get started.")