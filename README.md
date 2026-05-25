# LLM-Twin-MLOps: Private Domain-Specific RAG Pipeline

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-blue?style=for-the-badge)](https://ollama.com/)
[![LangChain](https://img.shields.io/badge/LangChain-v0.3-white?style=for-the-badge)](https://python.langchain.com/)

A production-grade Retrieval-Augmented Generation (RAG) pipeline designed to build a "Digital Twin" of a software engineer. This system ingests specialized technical knowledge (Angular components, RxJS patterns, documentation) and serves context-aware responses through a local Small Language Model (SLM).

---

## Architecture Overview

The project implements a "Zero-Cloud" architecture to ensure 100% data privacy and zero inference costs.

* Ingestion Layer: Automates the processing of .ts, .html, and .md files using DirectoryLoader and RecursiveCharacterTextSplitter.
* Vector Engine: Qdrant (Local Mode) stores document embeddings for high-speed semantic retrieval.
* Inference Layer: Ollama orchestrates Phi-3, a 3.8B parameter model optimized for reasoning on consumer-grade hardware.
* Serving Layer: FastAPI provides a RESTful interface with structured logging, Pydantic validation, and CORS middleware for frontend integration.

---

## Project Structure

llm-twin-mlops/
├── config/             # Centralized settings and path management
├── data_pipeline/      # Core logic: Ingestion, Retrieval, and Inference
├── my_knowledge/       # Source directory for technical knowledge (Code/Docs)
├── local_db/           # Persistent Vector Database (Git ignored)
├── src/
│   └── serving/        # FastAPI application and API routes
├── .env                # Environment variables (Git ignored)
└── requirements.txt    # Project dependencies

---

## Installation & Setup Guide

1. Model Preparation (Ollama)
The inference engine runs locally to ensure data privacy.
- Download and install Ollama for Windows (https://ollama.com/download).
- Open PowerShell and pull the Phi-3 model (optimized for systems with < 8GB RAM):
  ollama pull phi3
- (Cleanup) If you previously downloaded larger models that exceeded your RAM:
  ollama rm llama3

2. Python Environment Setup
- Clone the repository and navigate to the root:
  git clone https://github.com/your-username/llm-twin-mlops.git
  cd llm-twin-mlops
- Create and activate a virtual environment:
  python -m venv venv
  .\venv\Scripts\activate
- Install the required MLOps stack:
  pip install -r requirements.txt

3. Knowledge Base Preparation
Place your technical files (Angular components, READMEs, or documentation) into the my_knowledge/ folder. The pipeline is configured to parse .ts, .html, and .md formats.

---

## Running the Pipeline

Step 1: Sync the Knowledge Base
This processes your documents, creates semantic chunks, and updates the local vector store:
python -m data_pipeline.ingest

Step 2: Start the AI Service (FastAPI)
Launch the backend server to expose the Twin as a REST API:
python -m src.serving.app

Step 3: Verify & Query
Navigate to http://localhost:8000/docs. Use the interactive Swagger UI to test the /ask endpoint with a query such as: 
{"question": "How should I implement authentication interceptors?"}

---

## Technical Highlights

* Lifespan Management: Uses FastAPI lifespan to initialize the LLM and Vector DB once at startup, preventing memory overhead and reducing response latency.
* Semantic Chunking: Implements RecursiveCharacterTextSplitter with a 600 character limit and 100 character overlap to maintain context across complex code logic.
* Cross-Platform Compatibility: Uses Python's pathlib for dynamic path resolution, ensuring the code runs seamlessly on Windows, WSL, or Linux.
* Production Patterns:
    - CORS Middleware: Enabled for seamless integration with Angular/React frontends.
    - Pydantic Validation: Strict request/response schemas to prevent malformed data from reaching the model.
    - Structured Logging: Replaces standard print with Python logging for professional observability.
* Hardware-Aware AI: Specifically tuned for consumer-grade laptops by leveraging quantized Small Language Models (SLMs) that fit within 4GB of available RAM.

---

## License
Distributed under the MIT License.
