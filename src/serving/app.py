import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from data_pipeline.twin_engine import LLMTwin

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("TwinAPI")

# --- Schemas ---
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, example="How do I use RxJS with Angular interceptors?")

class QueryResponse(BaseModel):
    answer: str
    status: str = "success"

# --- Lifecycle Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing LLM Twin Engine...")
    app.state.twin = LLMTwin()
    yield
    logger.info("Shutting down resources...")

app = FastAPI(
    title="LLM Digital Twin API",
    description="Backend service for local RAG-based AI Twin",
    version="1.0.0",
    lifespan=lifespan
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
@app.get("/health", tags=["System"])
async def health_check():
    """Service discovery and monitoring endpoint."""
    return {"status": "operational", "version": "1.0.0"}

@app.post("/ask", response_model=QueryResponse, tags=["AI Core"])
async def ask_twin(request: QueryRequest):
    """
    Primary endpoint to query the Digital Twin.
    Retrieves context from local Qdrant and generates a response via Phi-3.
    """
    try:
        logger.info(f"Received query: {request.question[:50]}...")
        
        # Access the twin instance from app state
        response_text = app.state.twin.ask(request.question)
        
        return QueryResponse(answer=response_text)
    
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing the AI request."
        )

if __name__ == "__main__":
    uvicorn.run("src.serving.app:app", host="0.0.0.0", port=8000, reload=True)