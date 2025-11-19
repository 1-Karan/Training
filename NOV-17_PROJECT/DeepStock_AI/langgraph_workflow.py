from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import Optional
import matplotlib.pyplot as plt
import io, base64
import yfinance as yf

from modules.stock_data import get_stock_data
from modules.news_fetcher import get_stock_news
from modules.embedding import embed_and_store_news
from modules.chromadb_handler import search_similar_articles
from modules.llm_insights import generate_news_summary, generate_stock_insights
from modules.utils import extract_stock_symbol
from modules.sentiment_analyser1 import analyze_sentiment

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


# Define the state schema
class StockWorkflowState(BaseModel):
    user_query: str
    stock_symbol: str = None
    stock_data: list[dict] = None
    news_articles: list = None
    embedded_news: list = None
    similar_articles: list = None
    sentiment_results: list = None
    news_summary: str = None
    insights: str = None
    chart_base64: Optional[str] = None

# Define state functions
def extract_symbol(state: StockWorkflowState):
    symbol = extract_stock_symbol(state.user_query)
    return {"stock_symbol": symbol}

def fetch_data(state: StockWorkflowState):
    data = get_stock_data(state.stock_symbol)
    if not data:
        raise ValueError(f"No stock data found for symbol: {state.stock_symbol}")
    return {"stock_data": data}


def fetch_news(state: StockWorkflowState):
    articles = get_stock_news(state.stock_symbol)
    return {"news_articles": articles}

def embed_news(state: StockWorkflowState):
    embed_and_store_news(state.news_articles)  # Replace `None` with actual client if needed
    return {"embedded_news": state.news_articles}

def search_similar(state: StockWorkflowState):
    results = search_similar_articles(state.user_query)
    return {"similar_articles": results}

def sentiment_step(state):
    analyzed = analyze_sentiment(state.similar_articles)
    return {"sentiment_results": analyzed}

def summarize(state: StockWorkflowState):
    summary = generate_news_summary(state.similar_articles)
    return {"news_summary": summary}

def generate_insights(state: StockWorkflowState):
    insights = generate_stock_insights(state.stock_data, state.news_summary)
    return {"insights": insights}

def generate_chart(state: StockWorkflowState):
    import yfinance as yf, matplotlib.pyplot as plt, io, base64

    # Clean symbol
    stock_symbol = state.stock_symbol.strip().replace(" ", "").upper()
    if not stock_symbol.endswith(".NS"):
        stock_symbol += ".NS"

    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="60d")

    if hist.empty:
        print(f"No data found for {stock_symbol}")
        return {"chart_base64": ""}

    closes = hist.tail(30)["Close"]
    dates = closes.index.strftime("%Y-%m-%d").tolist()

    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, closes.values, marker="o", linestyle="-", color="blue")
    ax.set_title(f"{stock_symbol} - Last 30 Closing Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price (INR)")
    fig.autofmt_xdate()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    chart_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return {"chart_base64": chart_base64}



# Build the graph
graph = StateGraph(StockWorkflowState)

# Add states
graph.add_node("extract_stock_symbol", extract_symbol)
graph.add_node("fetch_stock_data", fetch_data)
graph.add_node("generate_chart", generate_chart)
graph.add_node("fetch_news", fetch_news)
graph.add_node("embed_news", embed_news)
graph.add_node("similarity_search", search_similar)
graph.add_node("sentiment_analysis", sentiment_step)
graph.add_node("summarize_news", summarize)
graph.add_node("generate_insights", generate_insights)

# Define transitions
graph.set_entry_point("extract_stock_symbol")
graph.add_edge("extract_stock_symbol", "fetch_stock_data")
graph.add_edge("fetch_stock_data", "generate_chart")
graph.add_edge("generate_chart", "fetch_news")
graph.add_edge("fetch_news", "embed_news")
graph.add_edge("embed_news", "similarity_search")
graph.add_edge("similarity_search", "sentiment_analysis")
graph.add_edge("sentiment_analysis", "summarize_news")
graph.add_edge("summarize_news", "generate_insights")

# Compile the workflow
workflow = graph.compile()
