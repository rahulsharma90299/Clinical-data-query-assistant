import streamlit as st
from clinical_workflow import clinical_graph


st.set_page_config(
    page_title="Clinical Data Query Assistant",
    page_icon="🧬",
    layout="centered"
)

st.title("Clinical Data Query Assistant")

st.write(
    "Ask questions about clinical data concepts "
    "using the available reference document."
)

st.info(
    "This assistant uses semantic retrieval and "
    "evidence-based answering. It will abstain "
    "when sufficient evidence is unavailable."
)

with st.form("question_form"):
    question = st.text_input(
        "Enter your clinical data question:",
        placeholder="e.g. What is SAE reconciliation?"
    )

    submitted = st.form_submit_button("Ask Question")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Analysing your question..."):
                response_data = clinical_graph.invoke(
                    {
                        "question": question.strip(),
                        "status": "",
                        "answer": ""
                    }
                )

            status = response_data.get("status")
            answer = response_data.get("answer", "")

            st.subheader("Response")

            if status == "answered":
                st.success("Status: Answered")
            else:
                st.warning("Status: Insufficient Evidence")

            st.write(answer)

        except Exception as error:
            st.error(f"Something went wrong: {error}")

st.divider()

st.caption(
    "Clinical Data Query Assistant | "
    "Built with Python, Semantic RAG and Ollama"
)
