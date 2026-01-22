import os
import tiktoken

MD_DOCS_DIR = "data/md_docs"
CHUNK_SIZE = 600
OVERLAP = 100

encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(text):
    tokens = encoding.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk = encoding.decode(tokens[start:end])
        chunks.append(chunk)
        start += CHUNK_SIZE - OVERLAP

    return chunks

def load_chunks():
    all_chunks = []

    for file in os.listdir(MD_DOCS_DIR):
        if file.endswith(".md"):
            with open(os.path.join(MD_DOCS_DIR, file), "r", encoding="utf-8") as f:
                text = f.read()

            for chunk in chunk_text(text):
                all_chunks.append({
                    "text": chunk,
                    "source": file
                })

    return all_chunks

if __name__ == "__main__":
    chunks = load_chunks()
    print(f"Total chunks created: {len(chunks)}")
