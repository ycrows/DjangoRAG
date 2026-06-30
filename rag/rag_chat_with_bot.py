import requests
import json
from .rag_retrieval import rag_retrieval

import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]


def generate_answer(query, context_docs):
    # Build a context string from the reranked documents
    context = "\n\n".join(
        f"[{i+1}] {doc['document']['text']}" #example: [1] RAG stands for Retrieval-Augmented Generation.
        for i, doc in enumerate(context_docs) 
    ) # what happens is that context will be a list of formatted string like in the example above

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
    retrieved_docs = rag_retrieval(query)

    answer = generate_answer(query, retrieved_docs) #answer = generate_answer(query, reranked)
    print(f"Question: {query}")
    print(f"Answer: {answer}")

    return answer
