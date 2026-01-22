import os
import pickle
import numpy as np
import faiss
from dotenv import load_dotenv
from openai import AzureOpenAI
from chunk_md import load_chunks

load_dotenv()

VECTOR_DB_DIR = "vectordb/faiss_index"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_EMBEDDING_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def get_embedding(text: str):
    response = client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=text
    )
    return response.data[0].embedding

def build_faiss_index():
    chunks = load_chunks()

    embeddings = []
    metadata = []

    for item in chunks:
        emb = get_embedding(item["text"])
        embeddings.append(emb)
        metadata.append(item)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, f"{VECTOR_DB_DIR}/index.faiss")

    with open(f"{VECTOR_DB_DIR}/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("✅ FAISS index created successfully")

if __name__ == "__main__":
    build_faiss_index()
