from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama

import logging
import os
from functools import lru_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")]
)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def load_vector_store():
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
            model_kwargs={"device": "cuda"}
        )
        vector_store_path = "/media/nsl3090-4/hdd/badhon/Chatbot/Part_3/vectorstore"
        db = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
        logger.info("Vector store loaded successfully")
        return db
    except Exception as e:
        logger.error(f"Failed to load vector store: {str(e)}")
        raise

@lru_cache(maxsize=1)
def load_llm():
    try:
        llm = Ollama(model=os.getenv("LLM_MODEL", "llama3.1:8b"))
        logger.info("LLM loaded successfully")
        return llm
    except Exception as e:
        logger.error(f"Failed to load LLM: {str(e)}")
        raise

def generate_answer(query: str) -> str:
    try:
        if not query:
            raise ValueError("Query cannot be empty")

        db = load_vector_store()
        llm = load_llm()
        retriever = db.as_retriever()


        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
        You are a professional banking assistant. Using only the provided context, answer the customer's question clearly and concisely without asking further questions.

        Context:
        {context}

        Question:
        {question}

        Answer:"""
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )

        answer = qa.run(query)
        logger.info(f"Generated answer for query: {query}")
        return answer.strip()
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        raise
