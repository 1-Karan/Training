import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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
    model="mistralai/mistral-7b-instruct:free",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# ------------------------------------------------------------
# 3. Define a helper tool (Summarization tool)
# ------------------------------------------------------------
def summarize(text: str) -> str:
    """Summarizes the given text."""
    prompt = f"Please summarize the following text in 2-3 sentences:\n\n{text}\n\nSummary:"
    try:
        response = llm.invoke(prompt)
        print("Full Response:", response)  # Debugging: log the full response
        return response.content.strip()  # Ensure the output is stripped of extra spaces
    except Exception as e:
        return f"Error: {str(e)}"

# ------------------------------------------------------------
# 4. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ------------------------------------------------------------
# 5. Set up a simple LLM chain
# ------------------------------------------------------------
prompt_template = "Summarize the following text into a concise summary: {text}"
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
summarization_chain = LLMChain(llm=llm, prompt=prompt)

# ------------------------------------------------------------
# 6. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your Agent ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Summarization command
    if user_input.lower().startswith("summarize"):
        text = " ".join(user_input.split()[1:]).strip()
        if text:
            try:
                # Using the updated summarize function with debugging
                summary = summarize(text)
                if summary:
                    print("Agent:", summary)
                else:
                    print("Agent: Sorry, I couldn't generate a summary.")
                memory.save_context({"input": user_input}, {"output": summary})
            except Exception as e:
                print("Error:", e)
        else:
            print("Agent: Please provide the text you want to summarize.")
        continue

    # Default: Respond to the user using LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)