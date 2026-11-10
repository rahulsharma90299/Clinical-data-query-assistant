
import streamlit as st
from clinical_graph import clinical_graph


# Page configuration
st.set_page_config(
    page_title="Clinical Data Query Assistant",
    page_icon="🩺",
    layout="centered"
)

# Application heading
st.title("🩺 Clinical Data Query Assistant")

st.write(
    "An AI-powered assistant that answers clinical "
    "data management questions using reference-based retrieval."
)

st.info(
    "This is an educational project. "
    "It is not an official SOP or a source of clinical advice."
)

st.divider()

# User question
question = st.text_input(
    "Enter your clinical data management question:",
    placeholder="Example: What is SAE reconciliation?"
)

# Submit question
if st.button("Submit Question", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Searching reference and generating response..."):

            result = clinical_graph.invoke({
                "question": question,
                "status": "",
                "answer": "",
                "decision": ""
            })

        st.subheader("Assistant Response")

        if result["status"] == "answered":
            st.success("Evidence found in reference")

        else:
            st.warning("Insufficient evidence")

        st.write(result["answer"])

        st.divider()

        st.subheader("Workflow Information")

        st.write("**Response status:**", result["status"])
        st.write("**LangGraph decision:**", result["decision"])

st.caption(
    "Powered by LangChain, LangGraph, Ollama and semantic retrieval."
)

