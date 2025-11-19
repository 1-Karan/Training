import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage

# Load environment variables
load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0  # strict factual extraction
)

def extract_stock_symbol(query: str) -> str:
    """
    Extract the stock/company name from a user query using Gemini LLM.

    Args:
        query (str): User input query (e.g., "What are the insights about TCS?")

    Returns:
        str: Extracted stock name or None if not found
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

    prompt = f"""
    You are a financial assistant. Extract ONLY the stock name or company name from this query.
    Rules:
    - Return ONLY the name like "Tata Motors" or "AAPL".
    - No explanation, punctuation, or extra text.
    - If no stock/company is mentioned, return "None".

    Query: {query}
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        stock_name = response.content.strip()


        if stock_name.lower() in ["none", "null", ""]:
            print("No valid stock name found in query.")
            return None
        return stock_name.lower()

    except Exception as e:
        print(f"Error extracting stock name: {e}")
        return None
