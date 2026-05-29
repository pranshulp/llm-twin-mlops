# LLM-Twin-MLOps: Private Domain-Specific RAG Pipeline

A production-grade Retrieval-Augmented Generation (RAG) pipeline designed to build a "Digital Twin" of a software engineer. This system ingests specialized technical knowledge (Angular components, RxJS patterns, documentation) and serves context-aware responses through a local Small Language Model (SLM).

---

## Architecture Overview

The project implements a "Zero-Cloud" architecture to ensure 100% data privacy and zero inference costs.

* Ingestion Layer: Automates the processing of .ts, .html, and .md files using DirectoryLoader and RecursiveCharacterTextSplitter.
* Parallel Processing: Scalable ingestion powered by Apache Beam for distributed data transformation.
* Vector Engine: Qdrant (Local Mode) stores document embeddings for high-speed semantic retrieval.
* Inference Layer: Ollama orchestrates Phi-3, a 3.8B parameter model optimized for reasoning on consumer-grade hardware.
* Serving Layer: FastAPI provides a RESTful interface with structured logging, Pydantic validation, and CORS middleware for frontend integration.

---

## Project Structure

llm-twin-mlops/\
  ├── config/             # Centralized settings and path management\
  ├── data_pipeline/      # Core logic: Ingestion, Retrieval, and Inference\
  ├── my_knowledge/       # Source directory for technical knowledge (Code/Docs)\
  ├── local_db/           # Persistent Vector Database (Git ignored)\
  ├── src/\
  │   └── serving/        # FastAPI application and API routes\
  ├── Dockerfile          # Containerization configuration\
  ├── docker-compose.yml  # Multi-container orchestration\
  ├── .env                # Environment variables (Git ignored)\
  └── requirements.txt    # Project dependencies

---

## Installation & Setup Guide

1. Model Preparation (Ollama)
The inference engine runs locally to ensure data privacy.
- Download and install Ollama for Windows (https://ollama.com/download).
- Open PowerShell and pull the Phi-3 model:
  ollama pull phi3

2. Standard Local Setup
- Clone the repository:
  git clone https://github.com/pranshulp/llm-twin-mlops.git
  cd llm-twin-mlops
- Create and activate a virtual environment:
  python -m venv venv
  .\venv\Scripts\activate
- Install dependencies:
  pip install -r requirements.txt

3. Docker Setup (Recommended)
To run the entire backend in a containerized environment:
docker-compose up --build

---

## Running the Pipeline

Step 1: Sync the Knowledge Base
You can run the standard ingestion or the parallelized Beam version:
# Standard
python -m data_pipeline.ingest
# Parallel
python -m data_pipeline.beam_ingest

Step 2: Start the AI Service
python -m src.serving.app

---

## Technical Highlights

* Lifespan Management: Uses FastAPI lifespan to initialize the LLM and Vector DB once at startup, preventing memory overhead.
* Parallel Data Pipelines: Implementation of Apache Beam for scalable document processing.
* Containerization: Full Docker support with optimized layer caching and volume persistence for local databases.
* Workflow Orchestration: Designed for integration with Apache Airflow or Prefect for automated daily syncs.
* Production Patterns:
    - CORS Middleware: Enabled for seamless integration with Angular/React frontends.
    - Pydantic Validation: Strict schemas for robust API interactions.
    - Structured Logging: Professional observability replacing standard print statements.
* Hardware-Aware AI: Specifically tuned for systems with < 8GB RAM using quantized SLMs (Phi-3).

---

## License
Distributed under the MIT License.
