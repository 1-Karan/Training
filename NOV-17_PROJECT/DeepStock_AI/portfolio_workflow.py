from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import io, base64
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import time

# -------------------- Setup --------------------

load_dotenv()

# Load OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# -------------------- State --------------------
class StockInput(BaseModel):
    symbol: str
    quantity: int

class PortfolioWorkflowState(BaseModel):
    portfolio: List[StockInput]
    risk: str
    sector_breakdown: Dict[str, int] = {}
    sector_chart_base64: Optional[str] = None
    ai_insights: Optional[str] = None
    recommendations: Optional[str] = None

# -------------------- Sector Analyzer --------------------
def sector_analyzer(state: PortfolioWorkflowState):
    stock_details = []
    sector_data = {}

    for stock in state.portfolio:
        prompt = f"""
        Identify the SECTOR ONLY STRICTLY for this Indian stock symbol: {stock.symbol}.
        Only return the sector name (e.g., IT, Energy, Banking, FMCG, Pharma, Metals, Auto, Telecom).
        If unknown, guess based on the company name.
        """
        sector = llm.invoke(prompt).content.strip()
        stock_details.append({"symbol": stock.symbol, "quantity": stock.quantity, "sector": sector})
        sector_data[sector] = sector_data.get(sector, 0) + stock.quantity

    # Generate pie chart
    fig, ax = plt.subplots()
    ax.pie(sector_data.values(), labels=sector_data.keys(), autopct="%1.1f%%")
    ax.axis("equal")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    chart_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return {
        "sector_breakdown": sector_data,
        "sector_chart_base64": chart_base64,
        "portfolio": stock_details
    }

# -------------------- Diversification Recommender --------------------
def diversification_recommender(state: PortfolioWorkflowState):
    prompt=f"""
    The user's portfolio is: {state.portfolio}.
    Sector allocation: {state.sector_breakdown}.
    Risk appetite: {state.risk}.

    Provide in concise bullet points:
    1. 2–3 positive insights about current holdings.
    2. 2–3 future sectors to consider (EV, Renewable Energy, AI, PSUs).
    Keep it under 180 words.
    """

    prompt1 = f"""
    The user's portfolio is: {state.portfolio}.
    Sector allocation: {state.sector_breakdown}.
    Risk appetite: {state.risk}.

    Provide:
    1. Diversification recommendations:
       - Top 3 mutual funds with 1-year returns and links.
       - Bonds (SGB, Gilt funds) with 1-year returns and links.
       - REITs and fixed-income options.
    In concise way in  very short and concise format approx 200-250 words and always give  approx 1 year return  as per you knowledge and DONT give LINKS strictty 
    """


    # Example: wait 6 seconds between requests

    response = llm.invoke(prompt).content.strip()
    time.sleep(6)
    response1 = llm.invoke(prompt1).content
    return {"ai_insights": response, "recommendations": response1}

# -------------------- Build Workflow --------------------
graph = StateGraph(PortfolioWorkflowState)

graph.add_node("sector_analyzer", sector_analyzer)
graph.add_node("diversification_recommender", diversification_recommender)

graph.set_entry_point("sector_analyzer")
graph.add_edge("sector_analyzer", "diversification_recommender")
graph.add_edge("diversification_recommender", END)

portfolio_workflow = graph.compile()
