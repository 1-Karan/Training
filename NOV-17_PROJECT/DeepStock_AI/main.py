# import streamlit as st
# from dotenv import load_dotenv
# import os
# from langgraph_workflow import workflow  # This is already a compiled graph
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Get API keys from environment variables
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
#
# # Set up Streamlit app
# st.title("Stock Insights with LangGraph and AI")
#
# # User input for query
# user_query = st.text_input("Enter your stock query (e.g., 'What are the insights about Tata Motors?')")
#
# # Button to process query
# if st.button("Get Insights"):
#     if user_query:
#         # Run the workflow with the user query
#         result = workflow.invoke({"user_query": user_query})
#
#         # Display results
#         st.write(f"### Current Stock Price for {result['stock_symbol']}: ₹{result['stock_data'][-1]['Close']}")
#         st.write(f"### 7-Day Stock Data:")
#         st.dataframe(result['stock_data'])
#         st.write(f"### News Summary:")
#         st.write(result['news_summary'])
#         st.write(f"### AI Insights:")
#         st.write(result['insights'])








#
# import streamlit as st
# from dotenv import load_dotenv
# import os
# from langgraph_workflow import workflow  # This is already a compiled graph
#
# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
#
# # Initialize session state for chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# # Streamlit app title
# st.title("Stock Insights Chatbot with LangGraph and AI")
#
# # User input
# user_query = st.text_input("Enter your stock query (e.g., 'Insights about Tata Motors?')")
#
# # Button to submit query
# if st.button("Send"):
#     if user_query:
#         # Invoke workflow for current query
#         result = workflow.invoke({"user_query": user_query})
#
#         # Prepare response
#         response = {
#             "query": user_query,
#             "stock_symbol": result.get("stock_symbol", "N/A"),
#             "stock_data": result.get("stock_data", []),
#             "news_summary": result.get("news_summary", ""),
#             "insights": result.get("insights", "")
#         }
#
#         # Append to chat history
#         st.session_state.chat_history.append(response)
#
# # Display chat history like a conversation
# for chat in reversed(st.session_state.chat_history):
#     st.markdown(f"**You:** {chat['query']}")
#     if chat['stock_data']:
#         st.markdown(f"**Current Stock Price for {chat['stock_symbol']}:** ₹{chat['stock_data'][-1]['Close']}")
#         st.markdown("**7-Day Stock Data:**")
#         st.dataframe(chat['stock_data'])
#     if chat['news_summary']:
#         st.markdown("**News Summary:**")
#         st.write(chat['news_summary'])
#     if chat['insights']:
#         st.markdown("**AI Insights:**")
#         st.write(chat['insights'])
#     st.markdown("---")





#
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from typing import Optional
#
# import os
# from pydantic import BaseModel
# from typing import List
#
# from langgraph_workflow import workflow
# from portfolio_workflow import portfolio_workflow # your compiled graph
#
# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
#
# app = FastAPI(title="Stock Insights Chatbot API")
#
# # In-memory chat history (like session_state in Streamlit)
# chat_history = []
#
#
# # Request schema
# class QueryRequest(BaseModel):
#     user_query: str
#
#
# # Response schema
# class QueryResponse(BaseModel):
#     query: str
#     stock_symbol: str
#     stock_data: list | None
#     chart_base64: Optional[str] = None
#     news_summary: str | None
#     insights: str | None
#     sentiment_results: list | None
#
# class StockInput(BaseModel):
#     symbol: str
#     quantity: int
#
# class PortfolioRequest(BaseModel):
#     portfolio: List[StockInput]
#     risk: str   # e.g. "Low", "Moderate", "High"
#
#
# @app.post("/query", response_model=QueryResponse)
# def run_query(request: QueryRequest):
#     """
#     Endpoint to process a stock query and return insights.
#     """
#     try:
#         # Run workflow
#         result = workflow.invoke({"user_query": request.user_query})
#
#         response = {
#             "query": request.user_query,
#             "stock_symbol": result.get("stock_symbol", "N/A"),
#             "stock_data": result.get("stock_data", []),
#             "news_summary": result.get("news_summary", ""),
#             "sentiment_results": result.get("sentiment_results", []),
#             "insights": result.get("insights", ""),
#             "chart_base64": result.get("chart_base64", "")
#         }
#
#         # Save to history
#         chat_history.append(response)
#
#         return response
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @app.get("/history")
# def get_history():
#     """
#     Endpoint to fetch chat history.
#     """
#     return {"history": chat_history}
#
#
# @app.delete("/history")
# def clear_history():
#     """
#     Clear chat history.
#     """
#     chat_history.clear()
#     return {"message": "Chat history cleared"}
#
#
# @app.post("/portfolio-analysis")
# def analyze_portfolio(request: PortfolioRequest):
#     try:
#         result = portfolio_workflow.invoke({
#             "portfolio": [s.dict() for s in request.portfolio],
#             "risk": request.risk
#         })
#
#         return {
#             "portfolio": result.get("portfolio", []),
#             "sector_breakdown": result.get("sector_breakdown", {}),
#             "sector_chart_base64": result.get("sector_chart_base64", ""),
#             "ai_insights": result.get("ai_insights", ""),
#             "recommendations": result.get("recommendations", {})
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional,List
import os

from langgraph_workflow import workflow
from portfolio_workflow import portfolio_workflow # your compiled graph

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

app = FastAPI(title="Stock Insights Chatbot API")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# In-memory chat history
chat_history = []


# Request schema
class QueryRequest(BaseModel):
    user_query: str


# Response schema
class QueryResponse(BaseModel):
    query: str
    stock_symbol: str
    stock_data: list | None
    chart_base64: Optional[str] = None
    news_summary: str | None
    insights: str | None
    sentiment_results: list | None

class StockInput(BaseModel):
    symbol: str
    quantity: int

class PortfolioRequest(BaseModel):
    portfolio: List[StockInput]
    risk: str   # e.g. "Low", "Moderate", "High"


# Home route
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Render the home page using Jinja2Templates
    """
    return templates.TemplateResponse("index.html", {"request": request})


# Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """
    Render the dashboard page using Jinja2Templates
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Portfolio route
@app.get("/portfolio", response_class=HTMLResponse)
def dashboard(request: Request):
    """
    Render the dashboard page using Jinja2Templates
    """
    return templates.TemplateResponse("portfolio.html", {"request": request})


@app.post("/query", response_model=QueryResponse)
def run_query(request: QueryRequest):
    """
    Endpoint to process a stock query and return insights.
    """
    try:
        result = workflow.invoke({"user_query": request.user_query})

        response = {
            "query": request.user_query,
            "stock_symbol": result.get("stock_symbol", "N/A"),
            "stock_data": result.get("stock_data", []),
            "news_summary": result.get("news_summary", ""),
            "sentiment_results": result.get("sentiment_results", []),
            "insights": result.get("insights", ""),
            "chart_base64": result.get("chart_base64", "")
        }

        chat_history.append(response)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
def get_history():
    return {"history": chat_history}


@app.delete("/history")
def clear_history():
    chat_history.clear()
    return {"message": "Chat history cleared"}


@app.post("/portfolio-analysis")
def analyze_portfolio(request: PortfolioRequest):
    try:
        result = portfolio_workflow.invoke({
            "portfolio": [s.dict() for s in request.portfolio],
            "risk": request.risk
        })

        return {
            "portfolio": result.get("portfolio", []),
            "sector_breakdown": result.get("sector_breakdown", {}),
            "sector_chart_base64": result.get("sector_chart_base64", ""),
            "ai_insights": result.get("ai_insights", ""),
            "recommendations": result.get("recommendations", {})
        }
    except Exception as e:
        raise HTTPException(e)

