
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from semantic_rag import answer_question


# Define the workflow state
class ClinicalState(TypedDict):
    question: str
    status: str
    answer: str


# Step 1: Run the existing RAG pipeline
def retrieve_and_answer(state: ClinicalState):
    response = answer_question(state["question"])

    return {
        "status": response["status"],
        "answer": response["answer"]
    }


# Step 2: Route based on evidence sufficiency
def route_by_evidence(state: ClinicalState):
    if state["status"] == "answered":
        return "answered"

    return "insufficient_evidence"


# Step 3: Handle supported answers
def answer_node(state: ClinicalState):
    return state


# Step 4: Handle insufficient evidence
def refusal_node(state: ClinicalState):
    return state


# Build the graph
builder = StateGraph(ClinicalState)

builder.add_node("retrieve_and_answer", retrieve_and_answer)
builder.add_node("answer", answer_node)
builder.add_node("refuse", refusal_node)

builder.add_edge(START, "retrieve_and_answer")

builder.add_conditional_edges(
    "retrieve_and_answer",
    route_by_evidence,
    {
        "answered": "answer",
        "insufficient_evidence": "refuse"
    }
)

builder.add_edge("answer", END)
builder.add_edge("refuse", END)

clinical_graph = builder.compile()


# Test the workflow independently
if __name__ == "__main__":
    question = input("Enter a clinical data question: ")

    result = clinical_graph.invoke({
        "question": question,
        "status": "",
        "answer": ""
    })

    print("\nFinal status:", result["status"])
    print("Final answer:", result["answer"])
