import chromadb
from sentence_transformers import SentenceTransformer

# Initialize sentence transformer model
transformer = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client
chroma_client = chromadb.Client()

# Create or get a collection
collection = chroma_client.get_or_create_collection(name="news_embeddings")

# Function to embed news articles and store them in ChromaDB
def embed_and_store_news(news_articles):
    embeddings = [transformer.encode(article['content']) for article in news_articles]

    for idx, embedding in enumerate(embeddings):
        collection.add(
            embeddings=[embedding],
            metadatas=[{"title": news_articles[idx]['title']}],
            documents=[news_articles[idx]['content']],
            ids=[news_articles[idx]['url']]
        )

    return {"embedded_news": news_articles}
