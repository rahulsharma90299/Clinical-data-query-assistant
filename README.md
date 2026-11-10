# Clinical Data Query Assistant

A retrieval-augmented generation (RAG) application that answers clinical data management questions using a supplied reference document. It uses semantic search to retrieve relevant information, a local Ollama language model to generate evidence-based responses, and LangGraph to control the answer/refusal workflow.

## Project Overview

The Clinical Data Query Assistant is designed as an educational project inspired by clinical data management workflows.

Users can ask questions about clinical data concepts, such as:

- Clinical data queries
- Adverse Events (AE)
- Serious Adverse Events (SAE)
- SAE reconciliation
- Database lock

The assistant retrieves relevant sections from a reference document and generates a response based on the retrieved evidence. When the available evidence is insufficient, it abstains rather than guessing.

## Key Features

- **Semantic retrieval:** Uses text embeddings and cosine similarity to identify relevant reference sections.
- **Evidence-based answering:** Generates responses using retrieved reference content.
- **Abstention mechanism:** Rejects questions when the best retrieval match falls below the configured similarity threshold.
- **LangChain integration:** Uses `ChatOllama` to connect the application to a locally hosted Ollama chat model.
- **LangGraph workflow:** Uses a state graph to route questions to an answer or insufficient-evidence path.
- **Interactive interface:** Provides a Streamlit application for submitting questions and viewing responses.
- **Retrieval experiments:** Compares similarity thresholds and Top-K retrieval settings.
- **Answer evaluation:** Tests whether the assistant answers supported questions and abstains on unsupported ones.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Ollama | Local language model and embedding model runtime |
| LangChain | Chat model integration through ChatOllama |
| LangGraph | Workflow orchestration and conditional routing |
| Streamlit | Interactive web interface |
| Semantic Search | Reference retrieval using embeddings |
| Cosine Similarity | Similarity scoring |
| PowerShell | Local development environment |

## System Architecture

```text
              User Question
                    |
                    v
             Streamlit UI
                    |
                    v
          LangGraph Workflow
                    |
                    v
          Clinical RAG Pipeline
                    |
          +---------+---------+
          |                   |
          v                   v
    Question Embedding   Reference Embeddings
          |                   |
          +---------+---------+
                    |
                    v
          Cosine Similarity
                    |
                    v
           Retrieve Top-K
                    |
                    v
          Evidence Assessment
                    |
             +------+------+
             |             |
       Sufficient       Insufficient
        Evidence         Evidence
             |             |
             v             v
       LangChain       Abstention
        ChatOllama      Response
             |
             v
       Final Answer
```

## LangChain and LangGraph Integration

### LangChain

The project uses LangChain's `ChatOllama` integration to communicate with the locally hosted Ollama chat model.

The model receives the retrieved reference context and the user's question, with instructions to avoid unsupported claims.

### LangGraph

LangGraph manages the question-answering workflow through a state graph.

The current workflow includes:

1. **Retrieve and answer:** Calls the existing RAG pipeline.
2. **Evidence-based routing:** Checks the returned response status.
3. **Answer node:** Handles questions with sufficient evidence.
4. **Refusal node:** Handles questions where evidence is insufficient.

The graph uses conditional edges to determine the appropriate response path.

## Retrieval Evaluation

A retrieval configuration experiment was conducted to compare different similarity thresholds and Top-K values.

### Experiment settings

- Similarity thresholds: 0.50, 0.60 and 0.70
- Top-K values: 1, 2 and 3
- Test questions: 4
- Evaluation criterion: Whether the expected reference section was retrieved, or no section was returned for an unsupported question.

### Results

| Similarity Threshold | Top-K | Passed | Score |
|---:|---:|---:|---:|
| 0.50 | 1 | 3/4 | 75% |
| 0.50 | 2 | 3/4 | 75% |
| 0.50 | 3 | 3/4 | 75% |
| 0.60 | 1 | 4/4 | 100% |
| 0.60 | 2 | 4/4 | 100% |
| 0.60 | 3 | 4/4 | 100% |
| 0.70 | 1 | 3/4 | 75% |
| 0.70 | 2 | 3/4 | 75% |
| 0.70 | 3 | 3/4 | 75% |

**Preliminary observation:** A similarity threshold of 0.60 achieved the best result on this small test set. Top-K = 2 was retained as the project's current retrieval configuration.

These results are preliminary and should not be interpreted as evidence of general performance across larger or independent datasets.

## Answer Evaluation

The project also includes an answer evaluation script that tests supported and unsupported questions.

The evaluation checks:

- Whether the assistant returns the expected answer or refusal status.
- Whether selected expected keywords appear in supported answers.
- Whether unsupported questions are rejected.

The current evaluation is a lightweight rule-based check. It does not constitute a comprehensive assessment of factual accuracy, clinical validity or answer groundedness.

## Project Structure

clinical-data-query-assistant/
|
|-- streamlit_app.py          # Main Streamlit application
|-- clinical_graph.py         # LangGraph workflow and routing
|-- semantic_rag.py           # Semantic retrieval and answer generation
|-- clinical_reference.txt    # Educational reference document
|-- evaluate_retrieval.py     # Retrieval evaluation
|-- evaluate_answers.py       # Answer and abstention evaluation
|-- retrieval_experiments.py  # Retrieval configuration experiments
|-- README.md                 # Project documentation
|-- .gitignore                # Git exclusions
|
|-- app.py                    # Legacy application entry point
|-- clinical_workflow.py      # Legacy workflow implementation

## Running the Project Locally

### Prerequisites

- Python
- Ollama
- Required Python packages
- The configured Ollama chat and embedding models

### 1. Download the Ollama models

The current project configuration uses:

```powershell
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text
```

### 2. Install Python dependencies

```powershell
pip install streamlit langgraph langchain-ollama
```

### 3. Navigate to the project folder

```powershell
cd "$HOME\Documents\clinical-data-query-assistant"
```

### 4. Run the application

```powershell
python -m streamlit run streamlit_app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

### 5. Run the evaluation scripts

```powershell
python evaluate_retrieval.py
python evaluate_answers.py
python retrieval_experiments.py
```

## Limitations and Future Improvements

- Expand the reference document and evaluation dataset.
- Introduce a larger and more diverse set of test questions.
- Evaluate retrieval precision, recall and ranking quality.
- Implement more rigorous answer-grounding and factuality evaluation.
- Explore source citations and retrieved-context visibility in the interface.
- Investigate deployment options using cloud infrastructure.

## Disclaimer

This is an educational demonstration using a limited reference document. It is not an official clinical system, a validated clinical decision-support tool, an SOP, or a source of medical advice. It should not be used to make real clinical or patient-care decisions.