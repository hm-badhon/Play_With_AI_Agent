# 🏦 Intelligent Banking Chatbot

A professional, real-time **AI-powered banking assistant** built using **LangChain**, **FAISS**, **HuggingFace embeddings**, **FastAPI**, and **Streamlit**. 
This chatbot delivers instant, accurate answers to customer queries based on a custom FAQ dataset.

## 🚀 Features

- 🧠 **Retrieval-Augmented Generation (RAG)** using LangChain
- 📄 Custom FAQ dataset in **JSON** format
- 🗃️ Vector search with **FAISS**
- 💬 Natural language responses using **Ollama LLM (LLaMA3)**
- 🧾 Clear, concise, direct answers
- 🛡️ **Rate limiting** with SlowAPI
- 🌐 **CORS support** for frontend-backend communication
- 🎛️ **Streamlit frontend UI**
- ⚡ FastAPI-based backend server

## 📁 Project Structure
```python
banking_chatbot/
├── data/
│ └── banking_faq.json # Preprocessed JSON FAQ data
├── vectorstore/ # FAISS index saved locally
├── app/
│ ├── backend/
│ │ ├── main.py # FastAPI app
│ │ └── rag_chain.py # Core logic (vector store + LLM + QA)
│ ├── frontend/
│ │ └── ui.py # Streamlit app
├── app.log # Log file
├── create_vectorstore.py # Script to create vector DB from JSON
├── requirements.txt # Python dependencies
└── README.md
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/banking-chatbot.git
cd banking-chatbot

2. Create and Activate a Virtual Environment

3. Install Dependencies

    pip install -r requirements.txt

4. Create Vector Store from JSON:
    Make sure your banking_faq.json file is placed in the data/ directory.
    # Run script
    python create_vectorstore.py
5. Run FastAPI Backend
    cd app/backend
    uvicorn main:app --reload --port 8000
6. Run Streamlit Frontend
    In another terminal:
        cd app/frontend
        streamlit run ui.py
```

### 🔒 Environment Variables (Optional)
You can define a .env file or export these:
```bash
    EMBEDDING_MODEL=all-MiniLM-L6-v2
    LLM_MODEL=llama3.1:8b
    FAQ_JSON_PATH=data/banking_faq.json
    VECTOR_STORE_PATH=vectorstore
    BACKEND_URL=http://localhost:8000/chat
    FRONTEND_URL=http://localhost:8501
```
### 📦 Requirements
Python 3.9+

Ollama installed and running LLaMA3 or similar

GPU support (optional but recommended for embeddings)
