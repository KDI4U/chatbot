# 🤖 Enterprise AI RAG Chatbot Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-blue?logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Database-orange)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?logo=ollama&logoColor=white)](https://ollama.ai/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Session_Store-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, enterprise-grade AI Chatbot Backend powered by **Retrieval-Augmented Generation (RAG)**. Built with **FastAPI**, **LangChain**, and **ChromaDB**, utilizing local LLMs via **Ollama** (Qwen3 / Nomic-Embed) for private, zero-latency document ingestion and intelligent semantic conversations.

---

## 🌟 Key Architectural Features

- **⚡ Asynchronous FastAPI Framework**: Clean layered architecture separating routes, services, repositories, and models.
- **📚 Advanced RAG Pipeline**: End-to-end document ingestion pipeline supporting PDF processing, recursive text chunking, and metadata tagging.
- **🔍 Vector Database & Semantic Retrieval**: Embedded **ChromaDB** for lightning-fast similarity search and contextual vector retrieval.
- **🦙 Local LLM Inference with Ollama**: Complete privacy and zero API token costs running open-weight models (`qwen3:8b`, `nomic-embed-text`) locally.
- **💬 Persistent Chat Sessions & History**: Relational database storage (`PostgreSQL` / `SQLAlchemy` + `Alembic`) for multi-turn conversations and user session tracking.
- **🛡️ Secure File Handling**: Validated multi-part document upload endpoints for on-the-fly knowledge base indexing.

---

## 📂 Project Architecture

```
chatbot/
├── app/
│   ├── ai/                        # Prompt engineering & LLM client wrappers
│   ├── api/v1/endpoints/          # API route controllers (Chat, Documents, Health)
│   ├── core/                      # Application settings, security & configuration
│   ├── database/                  # SQLAlchemy database engine and session managers
│   ├── models/                    # Database models (ChatSession, Message, Document)
│   ├── rag/                       # RAG orchestration (Text splitters, Embeddings, Retriever)
│   ├── repositories/              # Database query abstraction layer
│   ├── schemas/                   # Pydantic schemas for request/response validation
│   ├── services/                  # Business logic (Chat service, Ingestion service)
│   └── utils/                     # Helper utilities and custom exceptions
│
├── tests/                         # Pytest test suite
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git rules protecting database and vector stores
├── alembic.ini                    # Database migration configuration
├── requirements.txt               # Project dependencies
├── run.py                         # Application development runner
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- PostgreSQL database
- [Ollama](https://ollama.ai/) installed and running locally

### 2. Pull Required Ollama Models
```bash
# Pull LLM and Embedding models
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

### 3. Installation

```bash
# Clone the repository
git clone https://github.com/KDI4U/chatbot.git
cd chatbot

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration

Copy `.env.example` to `.env` and adjust settings:
```bash
cp .env.example .env
```
```ini
APP_NAME=BSWAN AI API
DEBUG=True

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bswan_ai
DB_USER=postgres
DB_PASSWORD=your_password

# Ollama LLM Settings
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

### 6. Start the Server
```bash
python run.py
# Or with uvicorn directly:
uvicorn app.main:app --reload --port 8000
```
Interactive Swagger API documentation will be live at: `http://localhost:8000/docs`

---

## 🧪 Testing

Execute the test suite to verify embeddings and vector retrieval:
```bash
python test_embedding.py
python test_retriever.py
python test_vector.py
```

---

## 🔒 Security & Privacy Notice
All persistent vector embeddings (`vector_db/`), uploaded enterprise documents (`uploads/`), and database credentials (`.env`) are strictly excluded via `.gitignore` to protect sensitive organizational data.

---

## 📄 License
This project is licensed under the MIT License.

---

<div align="center">
  <b>Developed & Maintained by <a href="https://github.com/KDI4U">Kundan Kumar</a></b>
</div>
