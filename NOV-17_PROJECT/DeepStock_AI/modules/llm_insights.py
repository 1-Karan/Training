
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# # Get the Gemini API Key from the environment
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM (Google Generative AI)
import os
import requests
import yfinance as yf
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.api.types import Documents, Embeddings
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# # Load environment variables
# load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)



# Function to generate 5-bullet-point summary of news articles using LLM
def generate_news_summary(news_articles):
    article_text = "\n\n".join([f"Title: {article['title']}\nContent: {article['content']}" for article in news_articles])
    prompt = f"""
    Summarize the following news articles in 5 concise bullet points:
    {article_text}
    JUST GIVE SUMMARY NOT TELL THAT THIS YOUR 5 POINTS SUMMARY JUST PUNE SUMMARY IN 5-6 POINTS
    """
    response = llm.invoke(prompt)
    return response.content

# Function to generate stock insights using LLM
def generate_stock_insights(stock_data, news_summary):
    prompt = f"""
    Here is the 7-day stock data and news summary . 
    Please generate a short response summarizing the stock's outlook and suggest an action (buy, hold, sell) based on the data and news.

    Stock Data: {stock_data}
    News Summary: {news_summary}
    """
    response = llm.invoke(prompt)
    return response.content
