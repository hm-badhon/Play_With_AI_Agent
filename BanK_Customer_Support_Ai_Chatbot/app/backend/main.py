from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from rag_chain import generate_answer
import logging
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Banking Chatbot API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:8501")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class Query(BaseModel):
    query: str

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(query: Query, request: Request):
    try:
        if not query.query.strip():
            logger.warning("Empty query received")
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        logger.info(f"Processing query: {query.query}")
        answer = generate_answer(query.query)
        return {"response": answer}
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")