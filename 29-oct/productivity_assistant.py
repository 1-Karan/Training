# ============================================================
# Smart-Agent.py — Summarizer, Sentiment, NoteKeeper, Improver
# ============================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# ------------------------------------------------------------
# 2. Initialize the Mistral model via OpenRouter
# ------------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# ------------------------------------------------------------
# 3. Initialize Memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
notes = []  # Persistent notes (stored during runtime)

# ------------------------------------------------------------
# 4. Tool Functions
# ------------------------------------------------------------
def summarize_text(text: str) -> str:
    """Summarize a long passage using the LLM."""
    prompt = f"Summarize the following text in one short sentence:\n\n{text}"
    response = llm.invoke(prompt)
    return response.content.strip()

def analyze_sentiment(text: str) -> str:
    """Detect emotional tone (positive, neutral, or negative)."""
    prompt = f"""
You are an expert sentiment analyzer.
Classify the sentiment of the following text as one of: positive, neutral, or negative.
Respond with only one of those words — no extra explanation.

Text: "{text}"
"""
    try:
        response = llm.invoke(prompt)
        cleaned = (
            response.content.replace("<s>", "")
            .replace("</s>", "")
            .replace("[/s]", "")
            .strip()
            .lower()
        )

        # Handle empty or unrecognized responses
        if not cleaned:
            cleaned = "unknown"
        elif cleaned not in ["positive", "neutral", "negative"]:
            # Try to infer if model gave a descriptive phrase
            if "happy" in cleaned or "good" in cleaned or "great" in cleaned:
                cleaned = "positive"
            elif "sad" in cleaned or "depress" in cleaned or "bad" in cleaned:
                cleaned = "negative"
            else:
                cleaned = "neutral"

        return f"The sentiment is {cleaned}."

    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"


def add_note(note: str) -> str:
    """Store a personal note in memory."""
    note = note.strip().strip('"').strip("'")
    notes.append(note)
    return f"Noted: “{note}”"

def get_notes() -> str:
    """Retrieve all saved notes."""
    if not notes:
        return "You have no saved notes yet."
    formatted = "\n".join([f"{i+1}. {n}" for i, n in enumerate(notes)])
    return f"You currently have {len(notes)} note(s):\n{formatted}"

def improve_text(text: str) -> str:
    """Rewrite text to be clearer or more professional."""
    prompt = (
        f"Rewrite the following text to make it clearer, more concise, and professional:\n\n{text}\n\n"
        f"Respond with one short improved version."
    )
    response = llm.invoke(prompt)
    return f"Suggested rewrite: {response.content.strip()}"

# ------------------------------------------------------------
# 5. Conversational Loop
# ------------------------------------------------------------
print("\n=== Smart Agent (Summarizer | Sentiment | NoteKeeper | Improver) ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    try:
        # Summarizer Tool
        if user_input.lower().startswith("summarize"):
            text = user_input[len("summarize"):].strip()
            if not text:
                print("Agent: Please provide text to summarize.")
                continue
            summary = summarize_text(text)
            print("Agent:", summary)
            memory.save_context({"input": user_input}, {"output": summary})
            continue

        # Sentiment Analyzer Tool
        if user_input.lower().startswith("analyze"):
            text = user_input[len("analyze"):].strip()
            if not text:
                print("Agent: Please provide text to analyze.")
                continue
            sentiment = analyze_sentiment(text)
            print("Agent:", sentiment)
            memory.save_context({"input": user_input}, {"output": sentiment})
            continue

        # NoteKeeper Tool
        if user_input.lower().startswith("note"):
            note_text = user_input[len("note"):].strip()
            if not note_text:
                print("Agent: Please provide a note to store.")
                continue
            result = add_note(note_text)
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        if user_input.lower().startswith("get notes"):
            response = get_notes()
            print("Agent:", response)
            memory.save_context({"input": user_input}, {"output": response})
            continue

        # Text Improver Tool
        if user_input.lower().startswith("improve"):
            text = user_input[len("improve"):].strip()
            if not text:
                print("Agent: Please provide text to improve.")
                continue
            improved = improve_text(text)
            print("Agent:", improved)
            memory.save_context({"input": user_input}, {"output": improved})
            continue

        # Default: Chat memory + LLM
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})

    except Exception as e:
        print("Error:", e)
