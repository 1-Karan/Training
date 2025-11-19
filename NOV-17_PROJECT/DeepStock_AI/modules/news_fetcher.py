import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the NewsAPI key from the environment
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Base URL for NewsAPI
NEWSAPI_URL = "https://newsapi.org/v2/everything"


# Function to fetch the latest news articles for a given stock symbol using requests
def get_stock_news(stock_symbol):
    """
    Fetch the latest news articles related to a given stock symbol.

    Args:
    - stock_symbol (str): The stock symbol or company name to search for in the news.

    Returns:
    - list: A list of news articles related to the stock symbol.
    """
    # Define the parameters for the NewsAPI request
    params = {
        'q': stock_symbol,  # Query term (stock symbol or company name)
        'language': 'en',  # Language of the articles (English)
        'sortBy': 'publishedAt',  # Sort by publication date
        'pageSize': 100,  # Limit to the top 10 articles
        'apiKey': NEWSAPI_KEY  # API Key for NewsAPI
    }

    # Send the GET request to the NewsAPI
    response = requests.get(NEWSAPI_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and return the articles
        articles = response.json().get('articles', [])
        return articles
    else:
        # Handle failed request and return an empty list
        print(f"Error: Unable to fetch news. Status code {response.status_code}")
        return []


# Example usage (Can be removed later)
if __name__ == "__main__":
    stock_symbol = input("Enter the stock symbol (e.g., 'Tesla', 'Apple', etc.): ")
    news_articles = get_stock_news(stock_symbol)

    if news_articles:
        print(f"Found {len(news_articles)} articles related to {stock_symbol}:")
        for article in news_articles:
            print(f"- {article['title']} ({article['publishedAt']})")
            print(f"  Source: {article['source']['name']}")
            print(f"  URL: {article['url']}")
            print("-" * 80)
    else:
        print("No articles found or error occurred.")
