import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from loguru import logger
import uvicorn
import argparse

load_dotenv(dotenv_path=os.environ.get('ENV_FILE', '.env'), override=True)

from app.rag.config import setup_logger
from app.rag.ask import ask_question
from app.rag.train import train_index
from app.rag.doctor import check_system
from app.rag.test import test_rag

# Initialize FastAPI app
app = FastAPI(
    title="On-Premise RAG API",
    description="API for Retrieval-Augmented Generation",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QuestionRequest(BaseModel):
    question: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024
    top_k: Optional[int] = 5

class AnswerResponse(BaseModel):
    answer: str
    sources: Optional[List[Dict[str, Any]]] = None

class TrainRequest(BaseModel):
    source_dir: str
    index_name: Optional[str] = None
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200

class DoctorResponse(BaseModel):
    status: str
    details: Dict[str, Any]

class TestRequest(BaseModel):
    test_questions: Optional[List[str]] = None
    test_file: Optional[str] = None
    index_name: Optional[str] = None

class TestResponse(BaseModel):
    results: List[Dict[str, Any]]
    metrics: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "On-Premise RAG API is running"}

@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    try:
        result = ask_question(
            question=request.question,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_k=request.top_k
        )
        return result
    except Exception as e:
        logger.error(f"Error in ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train", status_code=200)
async def train(request: TrainRequest):
    try:
        result = train_index(
            source_dir=request.source_dir,
            index_name=request.index_name,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        return {"status": "success", "details": result}
    except Exception as e:
        logger.error(f"Error in train endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctor", response_model=DoctorResponse)
async def doctor():
    try:
        result = check_system()
        return {"status": "success", "details": result}
    except Exception as e:
        logger.error(f"Error in doctor endpoint: {str(e)}")
        return {"status": "error", "details": {"error": str(e)}}

@app.post("/test", response_model=TestResponse)
async def test(request: TestRequest):
    try:
        results, metrics = test_rag(
            test_questions=request.test_questions,
            test_file=request.test_file,
            index_name=request.index_name
        )
        return {"results": results, "metrics": metrics}
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def start_api(host: str = "0.0.0.0", port: int = 8000, log_level: str = "info", log_dir: str = "logs"):
    setup_logger(log_level=log_level, log_dir=log_dir)
    logger.info(f"Starting RAG API on {host}:{port}")
    uvicorn.run("app.api:app", host=host, port=port, reload=True)

def main():
    # Check if API dependencies are installed
    try:
        import fastapi
        import uvicorn
    except ImportError:
        import sys
        print("API dependencies not found. Please install with 'pip install pirag[api]'", file=sys.stderr)
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="Start the RAG API server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--log-level", type=str, default="info", 
                      choices=["debug", "info", "warning", "error", "critical"], 
                      help="Logging level")
    parser.add_argument("--log-dir", type=str, default="logs", help="Directory for log files")
    
    args = parser.parse_args()
    start_api(host=args.host, port=args.port, log_level=args.log_level, log_dir=args.log_dir)

if __name__ == "__main__":
    main() 