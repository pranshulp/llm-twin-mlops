# LLM-Twin-MLOps: Private Domain-Specific RAG Pipeline

A production-grade Retrieval-Augmented Generation (RAG) pipeline designed to build a "Digital Twin" of a software engineer. This system ingests specialized technical knowledge (Angular components, RxJS patterns, documentation) and serves context-aware responses through a local Small Language Model (SLM).

---

## Architecture Overview

The project implements a "Zero-Cloud" architecture to ensure 100% data privacy and zero inference costs.

* Ingestion Layer: Automates the processing of .ts, .html, and .md files using DirectoryLoader.
* Parallel Processing: Scalable ingestion powered by Apache Beam for distributed data transformation.
* Vector Engine: Qdrant (Local Mode) stores document embeddings for high-speed semantic retrieval.
* Inference Layer: Ollama orchestrates Phi-3, a 3.8B parameter model optimized for reasoning on consumer-grade hardware.
* Serving Layer: FastAPI provides a RESTful interface with structured logging, Pydantic validation, and CORS middleware.

---

## Project Structure

llm-twin-mlops/
├── config/             # Centralized settings (chunk size, model names)\
├── data_pipeline/      # Core logic: Beam Ingestion, Retrieval, and Inference\
├── dags/               # Workflow Orchestration (Airflow/Prefect)\
├── my_knowledge/       # Source directory for technical knowledge\
├── local_db/           # Persistent Vector Database (Git ignored)\
├── src/\
│   └── serving/        # FastAPI application and API routes\
├── Dockerfile          # Containerization configuration\
├── docker-compose.yml  # Multi-container orchestration\
├── .env                # Environment variables\
└── requirements.txt    # Project dependencies\

---

## Installation & Setup Guide

1. Model Preparation (Ollama)
The inference engine runs locally to ensure data privacy.
- Download and install Ollama for Windows (https://ollama.com/download).
- Open PowerShell and pull the Phi-3 model:
  ollama pull phi3

2. Docker Setup (Recommended)
To run the containerized backend:
docker-compose up --build

3. Manual Local Setup
- Clone and enter the repo:
  git clone https://github.com/pranshulp/llm-twin-mlops.git
  cd llm-twin-mlops
- Create and activate a virtual environment:
  python -m venv venv
  .\venv\Scripts\activate
- Install dependencies:
  pip install -r requirements.txt

---

## Running the Pipeline

Step 1: Sync the Knowledge Base
Choose the ingestion method suited for your data scale:
# Standard Ingestion
python -m data_pipeline.ingest
# Parallel Ingestion
python -m data_pipeline.beam_ingest

Step 2: Automation (Optional)
If you have Airflow or Prefect installed, you can trigger the automated sync:
# Example for Prefect
python -m data_pipeline.orchestrator

Step 3: Start the AI Service
python -m src.serving.app

---

## Technical Highlights

* Parallel Data Pipelines: Implementation of Apache Beam for scalable document processing.
* Containerization: Full Docker support with volume persistence for the local vector store.
* Lifespan Management: FastAPI lifespan handles model and DB initialization efficiently.
* Hardware-Aware AI: Optimized for consumer-grade hardware using quantized SLMs (< 4GB RAM).
* Cross-Platform Compatibility: Dynamic path resolution for Windows, WSL, and Linux.

---

## License
Distributed under the MIT License.
