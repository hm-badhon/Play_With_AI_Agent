import json
import os
import logging
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")]
)
logger = logging.getLogger(__name__)

def create_vector_store():
    try:
        json_path = os.getenv("FAQ_JSON_PATH", "data/banking_faq.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON file not found at {json_path}")

        # Load JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert to list of Document objects
        documents = [Document(page_content=item['answer'], metadata={"question": item['question']}) for item in data]
        logger.info(f"Loaded {len(documents)} documents from JSON")

        # Embedding model
        embeddings = HuggingFaceEmbeddings(model_name=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"))
        
        # Create FAISS index
        db = FAISS.from_documents(documents, embeddings)
        vector_store_path = os.getenv("VECTOR_STORE_PATH", "vectorstore")
        db.save_local(vector_store_path)
        logger.info(f"Vector store saved to {vector_store_path}")
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}")
        raise

if __name__ == "__main__":
    create_vector_store()
