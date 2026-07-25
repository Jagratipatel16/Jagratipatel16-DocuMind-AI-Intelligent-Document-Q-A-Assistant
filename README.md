# 📄 DocuMind AI — Intelligent Document Q&A Assistant

DocuMind AI is a full-stack Retrieval-Augmented Generation (RAG) application that lets users upload PDF documents and ask natural-language questions about their content, with answers grounded in the actual document text and page-level citations.

## ✨ Features

- 🔐 **User Authentication** — register, login, logout with hashed passwords
- 📄 **Multi-PDF Upload** — upload and query multiple documents in one session
- 💬 **Conversational Chat UI** — ChatGPT-style chat bubbles with persistent conversation history
- 🧠 **RAG Pipeline** — PDF → chunking → embeddings → vector search → LLM-generated answer
- 📚 **Source Citations** — every answer shows which page(s) it was grounded in
- 📝 **AI Document Summarizer** — one-click structured summary of any uploaded PDF
- 📊 **Analytics Dashboard** — activity charts, conversation stats
- 👤 **Per-user Data Isolation** — each user's documents and chat history are private, backed by separate ChromaDB collections
- 🎨 **Custom themed UI** — consistent branding across every page
- ⚡ **Hybrid architecture** — local embeddings (Ollama, no per-query cost) + fast cloud inference (Groq) for answers

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App Framework | [Streamlit](https://streamlit.io/) |
| LLM (answer generation + summarization) | [Groq](https://groq.com/) — Llama 3.3 70B (cloud) |
| Embeddings | [Ollama](https://ollama.com/) — `nomic-embed-text` (local) |
| RAG Framework | [LangChain](https://www.langchain.com/) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) — per-user isolated collections |
| PDF Parsing | PyPDFLoader (`pypdf`) |
| Relational Database | MySQL + SQLAlchemy ORM |
| Charts | Plotly |
| Testing | Pytest |

## ✅ Prerequisites

- Python 3.10+
- MySQL Server running locally (or update `DB_HOST` for a remote instance)
- [Ollama](https://ollama.com/) installed and running locally, with the embedding model pulled:
  ```bash
  ollama pull nomic-embed-text
  ```
- A free [Groq API key](https://console.groq.com/keys)

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Jagratipatel16/Jagratipatel16-DocuMind-AI-Intelligent-Document-Q-A-Assistant.git
cd Jagratipatel16-DocuMind-AI-Intelligent-Document-Q-A-Assistant
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv documind-env
documind-env\Scripts\activate   # Windows
# source documind-env/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and fill in your own values:
```
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=documind_ai

GROQ_API_KEY=your_groq_api_key
```

### 4. Make sure Ollama is running
```bash
ollama serve
```

### 5. Set up the database
```bash
python -m database.create_tables
```

### 6. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 🧪 Testing

This project uses `pytest` for automated tests, covering authentication (`database/auth.py`), user CRUD operations, and the full conversation/chat-history flow.

```bash
pytest tests/
```

> Note: tests require the MySQL database to be reachable and tables created first (step 5 above).

## 📁 Project Structure

```
Jagratipatel16-DocuMind-AI-Intelligent-Document-Q-A-Assistant/
├── .streamlit/
│   └── config.toml           # App theme (colors, fonts)
├── app.py                    # Home page — upload PDFs, chat, summarize
├── session_utils.py          # Shared auth guard + theming for every page
├── pages/
│   ├── Login.py
│   ├── Register.py
│   ├── Chat.py                # Dedicated multi-conversation chat UI
│   ├── Dashboard.py           # Analytics dashboard
│   └── Profile.py
├── rag/
│   ├── loader.py               # PDF loading
│   ├── splitter.py             # Text chunking
│   ├── embeddings.py           # Ollama embedding model config
│   ├── vector_store.py         # ChromaDB storage (per-user isolated)
│   ├── retriever.py            # Similarity search
│   └── llm.py                   # Groq-based answer generation + summarization
├── database/
│   ├── database.py              # SQLAlchemy engine/session setup
│   ├── models.py                 # User, Conversation, ChatHistory models
│   ├── auth.py                   # Password hashing
│   ├── crud.py                   # User creation/lookup
│   ├── conversation_service.py
│   ├── chat_service.py
│   ├── history_service.py
│   └── create_tables.py          # DB table creation script
├── tests/
│   ├── test_auth.py              # Password hashing tests
│   ├── test_crud.py              # User creation/lookup tests
│   └── test_conversation_flow.py # End-to-end chat history tests
├── .env.example                  # Template for required environment variables
└── requirements.txt
```

## 🔒 Security Notes

- Passwords are hashed with `bcrypt` before storage
- Database and API credentials are loaded from environment variables (`.env`), never hardcoded
- `.env` is git-ignored and never committed
- Each user's uploaded documents live in an isolated ChromaDB collection — no cross-user data leakage

## 📌 Roadmap / Possible Future Additions

- [ ] OCR support for scanned/image-based PDFs
- [ ] Export chat as PDF/text
- [ ] Multi-language translation
- [ ] Suggested follow-up questions

## 👤 Author

**Jagrati Patel**
[GitHub](https://github.com/Jagratipatel16)