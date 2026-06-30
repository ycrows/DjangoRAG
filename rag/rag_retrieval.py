import requests
import json
import numpy as np

import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEXTS_FILE = BASE_DIR / "texts.json"

with open(TEXTS_FILE, "r", encoding="utf-8") as f:
    texts = json.load(f)
    f.close

EMBEDDINGS_FILE = BASE_DIR / "embeddings.npy"

embeddings = np.load(EMBEDDINGS_FILE)

# reconstruct the the document
document_embeddings = [
    {
        "text": text, 
        "embedding": embedding.tolist()}
    for text, embedding in zip(texts, embeddings)
]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, document_embeddings, top_n=5):
    # Embed the query
    response = requests.post( #use requests.post because we're sending to openrouter's web API, use post because we send information
        "https://openrouter.ai/api/v1/embeddings", # destination
        headers={ #authentication (actually optional in request.post but needed here)
            "Authorization": f"Bearer {OPENROUTER_API_KEY}", #who is the user
            "Content-Type": "application/json", #what is being sent
        },
        json={ #the content being sent
            "model": "openai/text-embedding-3-small",
            "input": query,
        },
    )

    #print(response.text)

    query_embedding = np.array(response.json()["data"][0]["embedding"])

    # Score each document by cosine similarity
    scored = []
    # blud looping through everything in the doc and comparing it instead of using a cool algorithm like HNSW
    for doc in document_embeddings: # this uses cosine method (find why)
        score = cosine_similarity(query_embedding, np.array(doc["embedding"])) # so one is the question (query) and one is based on the document
        scored.append({"text": doc["text"], "score": float(score)})

    # Return the top N most similar chunks
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def rerank(query, documents, top_n=3):
    response = requests.post(
        "https://openrouter.ai/api/v1/rerank",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "cohere/rerank-v3.5",
            "query": query,
            "documents": documents,
            "top_n": top_n,
        },
    )

    data = response.json()
    return data["results"]


def rag_retrieval(query):
    results = retrieve(query, document_embeddings, top_n=5)

    print("Retrieved documents:")
    for i, r in enumerate(results):
        print(f"  {i+1}. (score: {r['score']:.4f}) {r['text']}")

    # Use the texts from the retrieval step
    retrieved_texts = [r["text"] for r in results]

    reranked = rerank(query, retrieved_texts, top_n=3) #reranked will output a json file

    print("Reranked documents:")
    for r in reranked:
        print(f"  Score: {r['relevance_score']:.4f} | {r['document']['text']}")

    return reranked