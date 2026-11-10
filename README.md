# Clinical Data Query Assistant (AI-Powered RAG)

## Overview

Clinical Data Management involves handling queries related to clinical data, adverse events, SAE reconciliation, and database management. Finding relevant information from reference documents can take time.

This project solves that problem by building an **AI-powered Clinical Data Query Assistant** that retrieves relevant information from a reference document and generates evidence-based answers.

The application allows users to ask questions related to clinical data management and provides:
- Relevant information from the reference document
- Context-based answers using an LLM
- Abstention when sufficient evidence is not available

---

## Tech Stack

- Python – Core application logic
- Streamlit – Interactive user interface
- LangChain – LLM integration using ChatOllama
- LangGraph – Workflow orchestration and conditional routing
- Ollama – Locally hosted language and embedding models
- Semantic Search – Embedding-based document retrieval
- Cosine Similarity – Retrieval relevance scoring

---

## Project Workflow

### Step 1: User Query
- Accepts a clinical data management question through the Streamlit interface.

### Step 2: Semantic Retrieval
- Converts the question into embeddings and retrieves relevant reference sections using cosine similarity.

### Step 3: Evidence Assessment
- Checks whether the retrieved information meets the configured similarity threshold.

### Step 4: Generate Response
- Uses the locally hosted LLM to generate an answer based on the retrieved context.
- If sufficient evidence is unavailable, the assistant abstains rather than guessing.

### Step 5: LangGraph Workflow
- Manages the answer and abstention paths through conditional routing.

---

## Evaluation

- Tests supported and unsupported questions.
- Compares different similarity thresholds and Top-K retrieval settings.
- Evaluates answer and abstention behaviour using a lightweight rule-based test suite.

---

## ▶️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/rahulsharma90299/Clinical-data-query-assistant.git
cd Clinical-data-query-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Ollama models

```bash
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text
```

Make sure Ollama is running locally.

### 4. Run the application

```bash
python -m streamlit run streamlit_app.py
```

Open the application at `http://localhost:8501`.

---

## Disclaimer

This is an educational project based on a limited reference document. It is not an official clinical system, validated clinical decision-support tool, or source of medical advice. It should not be used for real clinical or patient-care decisions.
