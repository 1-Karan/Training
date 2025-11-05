from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL")

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct-free",
    api_key=api_key,
    base_url=base_url,
)

print(llm.invoke("Say hello").content)
