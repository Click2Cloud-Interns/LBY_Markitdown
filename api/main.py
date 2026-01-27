import os
import pickle
import numpy as np
import faiss
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

app = FastAPI()

index = faiss.read_index("vectordb/faiss_index/index.faiss")
with open("vectordb/faiss_index/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

embed_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_EMBEDDING_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

chat_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_CHAT_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

class Question(BaseModel):
    question: str

def embed_query(text):
    response = embed_client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=text
    )
    return np.array(response.data[0].embedding).astype("float32")

@app.post("/ask")
def ask(q: Question):
    q_emb = embed_query(q.question).reshape(1, -1)
    _, indices = index.search(q_emb, 5)

    context = "\n\n".join(metadata[i]["text"] for i in indices[0])

    prompt = f"""
Context:
{context}

Question:
{q.question}
"""

    response = chat_client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a Ladki Behan Yojana assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": list(set(metadata[i]["source"] for i in indices[0]))
    }
