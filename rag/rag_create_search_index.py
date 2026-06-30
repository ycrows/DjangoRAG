import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

# Your documents, split into chunks
chunks = [
    "OpenRouter is a unified API gateway for LLMs. It aggregates models from multiple providers.",
    "RAG stands for Retrieval-Augmented Generation. It grounds LLM answers in external data.",
    "Embeddings convert text into numerical vectors that capture semantic meaning.",
    "Reranking uses a cross-encoder to re-score documents for a given query, improving precision.",
    "Vector databases like Pinecone, Weaviate, and Qdrant store embeddings for fast similarity search.",
    "Prompt caching can reduce costs by reusing previous computations for repeated prefixes.",
    "OpenRouter supports provider routing to control which providers serve your requests.",
]

# Generate embeddings for all chunks in one batch request
response = requests.post(
    "https://openrouter.ai/api/v1/embeddings",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "openai/text-embedding-3-small",
        "input": chunks,
    },
)


#gotta find out what file is azure using to save the index
#separate and upload the index, make it so retrieval process can read the uploaded file
data = response.json()
# Each item in data["data"] contains an "embedding" vector
# Store these alongside your chunks in a vector database
document_embeddings = [
    {"text": chunks[item["index"]], "embedding": item["embedding"]}
    for item in data["data"]
]


# save it to a json and a numpy file
import numpy as np

embeddings = np.array([d["embedding"] for d in document_embeddings])
np.save("embeddings.npy", embeddings)

texts = [d["text"] for d in document_embeddings]
with open("texts.json", "w") as f:
    json.dump(texts, f)


print(f"Indexed {len(document_embeddings)} chunks with {len(document_embeddings[0]['embedding'])}-dim embeddings")
