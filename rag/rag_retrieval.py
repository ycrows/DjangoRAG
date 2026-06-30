import requests
import json
import numpy as np

import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

from elasticsearch import Elasticsearch
client = Elasticsearch(
    "https://my-elasticsearch-project-f38748.es.us-central1.gcp.elastic.cloud:443",
    api_key=os.environ["ELASTIC_API_KEY"],
)

def retrieve(query, top_n=5):
    # Embed the query
    query_response = requests.post( #use requests.post because we're sending to openrouter's web API, use post because we send information
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

    query_embedding = query_response.json()["data"][0]["embedding"]

    search_response = client.search(
        index="kibana_sample_data_vectordb_byoe",
        body={
            "knn": {
                "field": "content_embedding",
                "query_vector": query_embedding,
                "k": top_n,
                "num_candidates": 50
            }
        }
    )
    return search_response
