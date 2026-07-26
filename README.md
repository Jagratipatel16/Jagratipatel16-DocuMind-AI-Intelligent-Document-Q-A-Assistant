# 📄 DocuMind AI — Intelligent Document Q&A Assistant

DocuMind AI is a full-stack Retrieval-Augmented Generation (RAG) application that lets users upload PDF documents and ask natural-language questions about their content, with answers grounded in the actual document text and page-level citations.

## 🚀 Live Demo

[Try DocuMind AI](https://jagratipatel16-jagratipatel16-documind-ai-intelligen-app-zmscmk.streamlit.app/)

> Hosted on Streamlit Community Cloud with a MySQL database on Railway. Note: uploaded PDFs and vector data reset on app restart/redeploy — chat history and accounts persist since they live in the hosted database.

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
- ☁️ **Fully cloud-based AI** — embeddings (HuggingFace) and answer generation (Groq) both run via API, no local model server required, making it easy to deploy anywhere

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App Framework | [Streamlit](https://streamlit.io/) |
| Hosting | [Streamlit Community Cloud](https://streamlit.io/cloud) |
| LLM (answer generation + summarization) | [Groq](https://groq.com/) — Llama 3.3 70B (cloud) |
| Embeddings | [HuggingFace Inference API](https://huggingface.co/) — `sentence-transformers/all-MiniLM-L6-v2` (cloud) |
| RAG Framework | [LangChain](https://www.langchain.com/) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) — per-user isolated collections |
| PDF Parsing | PyPDFLoader (`pypdf`) |
| Relational Database | MySQL ([Railway](https://railway.app/)) + SQLAlchemy ORM |
| Charts | Plotly |
| Testing | Pytest |

## ✅ Prerequisites (for local development)

- Python 3.10+
- MySQL Server running locally (or point `DB_HOST` at a remote/hosted instance)
- A free [Groq API key](https://console.groq.com/keys) — for answer generation
- A free [HuggingFace access token](https://huggingface.co/settings/tokens) (Read permission) — for embeddings

## 🚀 Getting Started (local)

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
HF_TOKEN=your_huggingface_token
```

### 4. Set up the database
```bash
python -m database.create_tables
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## ☁️ Deployment

This app is deployed on **Streamlit Community Cloud**, with a **MySQL database hosted on Railway** (Streamlit Cloud's filesystem is ephemeral, so the database has to live externally).

Configuration values (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `GROQ_API_KEY`, `HF_TOKEN`) are set via Streamlit Cloud's **Secrets** manager instead of a `.env` file. Streamlit Cloud automatically exposes top-level Secrets as environment variables, so the app's existing `os.getenv()` calls work the same way both locally (reading from `.env`) and when deployed (reading from Secrets) — no extra code needed.

To deploy your own copy:
1. Push the repo to GitHub
2. Provision a MySQL database (e.g. on [Railway](https://railway.app/)) and run `python -m database.create_tables` against it once
3. Create a new app on [share.streamlit.io](https://share.streamlit.io), pointing at `app.py`
4. Add all required keys under **Advanced settings → Secrets**
5. Deploy

## 🧪 Testing

This project uses `pytest` for automated tests, covering authentication (`database/auth.py`), user CRUD operations, and the full conversation/chat-history flow.

```bash
pytest tests/
```

> Note: tests require the MySQL database to be reachable and tables created first (step 4 above).

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
│   ├── embeddings.py           # HuggingFace Inference API embedding config
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
- Database and API credentials are loaded from environment variables — a local `.env` file during development, or Streamlit Cloud's Secrets manager (auto-exposed as env vars) when deployed — never hardcoded
- `.env` is git-ignored and never committed
- Each user's uploaded documents live in an isolated ChromaDB collection — no cross-user data leakage

## 📌 Roadmap / Possible Future Additions

- [ ] OCR support for scanned/image-based PDFs
- [ ] Export chat as PDF/text
- [ ] Multi-language translation
- [ ] Suggested follow-up questions
- [ ] Persistent object storage for uploaded PDFs/vectors (survive redeploys)

## 👤 Author

**Jagrati Patel**
[GitHub](https://github.com/Jagratipatel16)