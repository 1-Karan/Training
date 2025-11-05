import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = "sk-or-v1-a1cb5b1865d702"

import requests
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub


# --- API CONFIG ---
os.environ["OPENROUTER_BASE_URL"] = "https://openrouter.ai/api/v1"
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "sk-or-v1")

API_URL = "http://127.0.0.1:8000"  # FastAPI backend

# --- TOOLS (same as before) ---
@tool
def get_doctors(query: str = "") -> str:
    """Fetch list of doctors from the FastAPI backend."""
    try:
        r = requests.get("http://127.0.0.1:8000/doctors")
        if r.status_code == 200:
            doctors = r.json()
            return "Available doctors:\n" + "\n".join(
                [f"{d['id']}: {d['name']} - {d['specialty']}" for d in doctors]
            )
        return "Error fetching doctors."
    except Exception as e:
        return f"Error: {e}"




@tool("get_available_slots")
def get_available_slots(doctor_id: str) -> str:
    """Fetch available slots for a doctor."""
    r = requests.get(f"{API_URL}/available-slots/{doctor_id}")
    if r.status_code == 200:
        data = r.json()
        slots = data.get("available_slots", [])
        return f"Available slots: {', '.join(slots)}" if slots else "No available slots."
    return "Doctor not found."


@tool("book_appointment")
def book_appointment(doctor_id: str, patient_name: str, time: str) -> str:
    """Book an appointment."""
    payload = {"doctor_id": doctor_id, "patient_name": patient_name, "time": time}
    r = requests.post(f"{API_URL}/book-appointment", json=payload)
    return r.json().get("message", "Error booking appointment.")


# --- CREATE LANGCHAIN AGENT (with Mistral model via OpenRouter) ---
def create_agent():
    """Create a modern ReAct agent for appointment management."""
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        temperature=0.4,
    )

    tools = [get_doctors, get_available_slots, book_appointment]

    # Local ReAct-style prompt (no LangSmith dependency)
    from langchain.prompts import PromptTemplate
    prompt = PromptTemplate.from_template("""
You are a helpful AI healthcare scheduling assistant.

You have access to the following tools:
{tool_names}

Tool details:
{tools}

When reasoning, follow this step-by-step process:
Thought: describe what you plan to do
Action: choose one of the tools
Action Input: provide the tool input
Observation: note the tool's response
... (repeat as needed)
Final Answer: summarize your final response to the user clearly.

User query:
{input}

{agent_scratchpad}

If you already have the final answer, just respond with 'Final Answer: <your answer>'.
""")

    # Build agent with error handling and retry limit
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3  # Retry up to 3 times before giving up
    )
    return executor




def run_agent():
    print("🩺 Healthcare Assistant (Mistral 7B via OpenRouter)")
    print("Try:")
    print("- Show me all available doctors")
    print("- What are the slots for dr_1?")
    print("- Book an appointment with dr_2 for Alex at 3:00 PM\n")

    agent = create_agent()

    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "stop"]:
            print("👋 Exiting assistant...")
            break
        response = agent.invoke({"input": query})
        print(f"AI: {response['output']}\n")



if __name__ == "__main__":
    run_agent()
