#  🌸 Ladli Behna Yojana (Markitdown VectorDB)

A Retrieval-Augmented Generation (RAG) chatbot built for the **Ladki Behan / Ladli Behna Yojana**.  
It converts government documents into Markdown, stores embeddings in a FAISS vector database, and answers user questions via a FastAPI backend using Azure OpenAI.

---

## ✨ Features

- 📄 Convert PDFs → Markdown using Microsoft MarkItDown
- ✂️ Chunk Markdown documents intelligently
- 🔎 Create embeddings using Azure OpenAI Embedding model
- 🧠 Store & search vectors using FAISS
- 💬 User-friendly Q&A API using FastAPI
- 📚 Source-aware answers (returns supporting documents)
- 🌐 Can be accessed from Postman or other machines on LAN

---

## 🏗️ Project Structure

```
ladki-behan-chatbot/
│
├── api/
│   ├── __init__.py
│   └── main.py                # FastAPI app (Q&A endpoint)
│
├── Data/
│   ├── raw/                   # Original PDF documents
│   └── md_docs/               # Converted Markdown files
│
├── ingestion/
│   ├── __init__.py
│   ├── convert_to_md.py       # PDF → Markdown (MarkItDown)
│   ├── chunk_md.py            # Markdown chunking
│   └── embed_store.py         # Embedding + FAISS storage
│
├── prompts/
│   └── qa_prompt.txt          # Prompt for user-friendly answers
│
├── vectordb/
│   └── faiss_index/           # FAISS index files
│
├── .env                       # Azure OpenAI credentials
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **FastAPI**
- **FAISS**
- **Azure OpenAI** (GPT + Embeddings)
- **MarkItDown** (Microsoft)
- **Uvicorn**
- **Postman** (for API testing)

---

## 🔐 Environment Variables (.env)

Create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=YOUR_API_KEY
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

⚠️ **Never commit `.env` to GitHub**

---

## 📦 Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 🔄 Data Ingestion Pipeline

Run these once (or when documents change):

### 1️⃣ Convert PDFs to Markdown

```bash
python ingestion/convert_to_md.py
```

### 2️⃣ Create embeddings & FAISS index

```bash
python ingestion/embed_store.py
```

✅ After this, your vector database is ready.

---

## 🚀 Run the API

From project root:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

---

## 🔗 API Usage

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### Ask a Question (POST)

**Endpoint:** `POST /ask`

**Request Body:**

```json
{
  "question": "Who is eligible for Ladki Behan Yojana?"
}
```

**Response:**

```json
{
  "answer": "Women aged 21–60 years who are residents of Madhya Pradesh and meet income criteria are eligible.",
  "sources": [
    "Policy Brief Mukhyamantri LBY Madhya Pradesh.md"
  ]
}
```

---

## 🌍 Access from Another PC

Run API with:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Then use:

```
http://<YOUR_PC_IP>:8000/ask
```

**Example:**

```
http://192.168.1.23:8000/ask
```

---

## 🧠 Prompt Customization

Edit:

```
prompts/qa_prompt.txt
```

Then restart the API to reflect changes:

```bash
CTRL + C
uvicorn api.main:app --reload
```

---

## 🛡️ Notes

- This project is **backend-only**
- No UI included
- Supports **Marathi / Hindi / English** content (depending on documents)
- Designed for government scheme knowledge assistance

---

