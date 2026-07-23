import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import requests

load_dotenv()

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

client = Elasticsearch(
    os.environ["ELASTIC_CLIENT"],
    api_key=os.environ["ELASTIC_API_KEY"],
)



mappings = {
    "properties": {
        "title": {
            "type": "text" # Full-text search via BM25.
        },
        "content": {
            "type": "text" # Stored for display and BM25 search. Embeddings are stored separately.
        },
        "content_embedding": {
            "type": "dense_vector", # Stores the raw vector (list of numbers) from your embedding model.
            "dims": 1536, # ⚠️ Must exactly match your model's output size. Wrong dims = full reindex to fix.
            "index": True, # Required for kNN search. Without this, vectors are stored but not searchable.
            "similarity": "cosine", # How Elasticsearch measures closeness between vectors. Cosine is the most common choice.
            "index_options": {
                "type": "int8_hnsw" # Compressed index type for ~4x memory savings. Use 'hnsw' for maximum accuracy.
            }
        },
        "source": {
            "type": "keyword" # Exact-match only. Used for filtering, e.g. tenant ID, category, document source.
        }
    }
}

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import BadRequestError

# Create the index, if it already exists, remove it and make a new one
try:
    client.indices.create(
        index="kibana_sample_data_vectordb_byoe",
        mappings=mappings
    )
    print("Index created.")

except BadRequestError as e:
    if e.error == "resource_already_exists_exception":
        print("Index already exists. Deleting and recreating...")

        client.indices.delete(index="kibana_sample_data_vectordb_byoe")

        client.indices.create(
            index="kibana_sample_data_vectordb_byoe",
            mappings=mappings
        )
        print("Index recreated.")
    else:
        raise

# Open document with data
from pathlib import Path
import json
BASE_DIR = Path(__file__).resolve().parent
TEXTS_FILE = BASE_DIR / "my_document.json"

with open(TEXTS_FILE, "r", encoding="utf-8") as f:
    my_document = json.load(f)
    f.close

document_content = [
    doc["_source"]["content"]
    for doc in my_document
]

# Send document content and convert into embedding
response = requests.post(
    "https://openrouter.ai/api/v1/embeddings",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "openai/text-embedding-3-small",
        "input": document_content,
    },
)
response.raise_for_status()

# Extract the converted embedding
embeddings = [
    item["embedding"] 
    for item in response.json()["data"]
]


from elasticsearch.helpers import bulk
# no need to reformat it into json structure because my_document is already in json structure
for doc, embedding in zip(my_document, embeddings):
    doc["_source"]["content_embedding"] = embedding

bulk(client, my_document)