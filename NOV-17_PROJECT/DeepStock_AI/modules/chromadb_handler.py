import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
client = chromadb.Client()

# Create or get a collection
collection = client.get_or_create_collection(name="news_embeddings")

# Initialize sentence transformer model for similarity search
transformer = SentenceTransformer('all-MiniLM-L6-v2')

# Function to perform similarity search for the user query
def search_similar_articles(query):
    query_embedding = transformer.encode(query)

    search_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=7
    )

    articles = []
    for i in range(len(search_results['documents'][0])):
        articles.append({
            "url": search_results['ids'][0][i],
            "content": search_results['documents'][0][i],
            "title": search_results['metadatas'][0][i].get("title", "Untitled"),
            "distance": search_results['distances'][0][i]
        })

    return articles




