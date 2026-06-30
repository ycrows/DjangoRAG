import requests
import json
from .rag_retrieval import retrieve

import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

# change the formatting from json format 
def format_context(search_response):
    docs = search_response["hits"]["hits"]

    context = []
    for i, hit in enumerate(docs, start=1):
        source = hit["_source"]

        context.append(
            f"""[Source {i}]
Title: {source['title']}
Content: {source['content']}
Dataset: {source['source']}
"""
        )

    return "\n\n".join(context)

def generate_answer(query, context_docs):
    context = format_context(context_docs)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "~openai/gpt-mini-latest",
            "messages": [
                {
                    "role": "system", #better not to switch the order even though we explicitly define the role
                    "content": "Answer the user's question based on the provided context. "
                               "Cite the relevant source numbers in brackets. "
                               "If the context doesn't contain enough information, say so."
                               #"If the context doesn't contain enough information, say so. But still try to answer with general knowledge",
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
            "max_tokens": 300,

        },
    )
    print(response.json()["usage"]) # how many tokens we using 
    return response.json()["choices"][0]["message"]["content"]



def chat_with_bot(query):
    retrieved_docs = retrieve(query)

    answer = generate_answer(query, retrieved_docs) 
    print(f"Question: {query}")
    print(f"Answer: {answer}")

    return answer
