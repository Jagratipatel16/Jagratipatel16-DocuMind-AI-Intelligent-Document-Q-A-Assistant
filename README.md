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
- 👤 **Per-user Data Isolation** — each user's documents and chat history are private
- 🎨 **Custom themed UI** — consistent branding across every page

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App Framework | [Streamlit](https://streamlit.io/) |
| LLM (answer generation) | [Groq](https://groq.com/) — Llama 3.3 70B |
| Embeddings | Google Gemini (`text-embedding-004`) |
| RAG Framework | [LangChain](https://www.langchain.com/) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| PDF Parsing | PyPDFLoader |
| Relational Database | MySQL + SQLAlchemy ORM |
| Charts | Plotly |

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd documind-ai
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv documind-env
documind-env\Scripts\activate   # Windows
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
GOOGLE_API_KEY=your_google_api_key
```

### 4. Set up the database
```bash
python database/create_tables.py
```

### 5. Run the app
```bash
streamlit run app.py
```

## 📁 Project Structure

```
documind-ai/
├── app.py                  # Home page — upload PDFs, chat, summarize
├── pages/
│   ├── Login.py
│   ├── Register.py
│   ├── Chat.py              # Dedicated multi-conversation chat UI
│   ├── Dashboard.py         # Analytics dashboard
│   └── Profile.py
├── rag/
│   ├── loader.py            # PDF loading
│   ├── splitter.py          # Text chunking
│   ├── embeddings.py        # Embedding model config
│   ├── vector_store.py      # ChromaDB storage (per-user isolated)
│   ├── retriever.py         # Similarity search
│   └── llm.py                # Answer generation + summarization
├── database/
│   ├── models.py             # SQLAlchemy models (User, Conversation, ChatHistory)
│   ├── crud.py                # Auth-related DB operations
│   ├── conversation_service.py
│   ├── chat_service.py
│   └── history_service.py
└── session_utils.py           # Shared auth guard + theming
```

## 🔒 Security Notes

- Passwords are hashed before storage
- Database credentials are loaded from environment variables, never hardcoded
- Each user's uploaded documents live in an isolated vector store collection

## 📌 Roadmap / Possible Future Additions

- [ ] OCR support for scanned/image-based PDFs
- [ ] Export chat as PDF/text
- [ ] Multi-language translation
- [ ] Suggested follow-up questions

## 👤 Author

**Jagrati Patel**
[GitHub](https://github.com/Jagratipatel16)