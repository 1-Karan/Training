import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API token from the environment
API_TOKEN = os.getenv("HF_API_TOKEN")

# Define the new API URL (this should be the latest one)
API_URL = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"


# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Function to classify text sentiment
def classify_text(text):
    payload = {"inputs": text}

    # Send a POST request to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
text = "I love this product, it's amazing!"
classification_result = classify_text(text)

print(classification_result)