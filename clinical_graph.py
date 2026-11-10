
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from semantic_rag import answer_question


# Define the information passed between graph nodes
class ClinicalState(TypedDict):
    question: str
    status: str
    answer: str
    decision: str


# Node 1: Run the existing RAG assistant
def run_assistant(state: ClinicalState):
    response = answer_question(state["question"])

    return {
        "status": response["status"],
        "answer": response["answer"]
    }


# Node 2: Handle supported answers
def answer_supported(state: ClinicalState):
    return {
        "decision": "Answer supported by reference"
    }


# Node 3: Handle insufficient evidence
def abstain_from_answering(state: ClinicalState):
    return {
        "decision": "Insufficient evidence - abstained"
    }


# Decide which node should run next
def route_response(state: ClinicalState):
    if state["status"] == "answered":
        return "supported"

    return "insufficient"


# Build the LangGraph workflow
workflow = StateGraph(ClinicalState)

workflow.add_node("run_assistant", run_assistant)
workflow.add_node("answer_supported", answer_supported)
workflow.add_node("abstain", abstain_from_answering)

workflow.add_edge(START, "run_assistant")

workflow.add_conditional_edges(
    "run_assistant",
    route_response,
    {
        "supported": "answer_supported",
        "insufficient": "abstain"
    }
)

workflow.add_edge("answer_supported", END)
workflow.add_edge("abstain", END)

clinical_graph = workflow.compile()


# Run the workflow
if __name__ == "__main__":
    question = input("Enter your clinical question: ")

    result = clinical_graph.invoke({
        "question": question,
        "status": "",
        "answer": "",
        "decision": ""
    })

    print("\nFinal result:")
    print("Status:", result["status"])
    print("Answer:", result["answer"])
    print("Graph decision:", result["decision"])
