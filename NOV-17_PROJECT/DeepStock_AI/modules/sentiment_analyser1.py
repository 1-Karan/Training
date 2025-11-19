from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load FinBERT model + tokenizer
MODEL_NAME = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Labels used by FinBERT
LABELS = ["positive", "negative", "neutral"]


def analyze_sentiment(articles):
    """
    Perform sentiment analysis on a list of articles using FinBERT.

    Args:
        articles (list[dict]): List of articles with keys 'title', 'content', 'url'.

    Returns:
        list[dict]: List of formatted results with sentiment label and score.
    """
    results = []

    for article in articles:
        # Take first 2 lines of content (or truncate if shorter)
        snippet = " ".join(article["content"].split(". ")[:2])

        # Encode content for sentiment analysis
        inputs = tokenizer(article["content"], return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)

        # Convert logits to probabilities
        probs = F.softmax(outputs.logits, dim=-1)
        score, label_id = torch.max(probs, dim=1)

        sentiment_label = LABELS[label_id.item()]
        sentiment_score = score.item()

        # Format result
        results.append({
            "title": article["title"],
            "snippet": snippet,
            "url": article["url"],
            "sentiment": sentiment_label,
            "score": round(sentiment_score, 4)
        })

    return results
