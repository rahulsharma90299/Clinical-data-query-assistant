
import json
import math
from pathlib import Path
from urllib.request import Request, urlopen
from langchain_ollama import ChatOllama, OllamaEmbeddings

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen2.5:1.5b"
BASE_URL = "http://localhost:11434"
chat_model = ChatOllama(
    model=CHAT_MODEL,
    temperature=0,
    format="json"
)

embedding_model = OllamaEmbeddings(
    model=EMBED_MODEL
)

def call_ollama(endpoint, payload):
    request = Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def get_embedding(text):
    return embedding_model.embed_query(text)


def cosine_similarity(vector_a, vector_b):
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


# Load the reference document and split it into sections
document = Path("clinical_reference.txt").read_text(encoding="utf-8")

chunks = [
    section.strip()
    for section in document.split("\n## ")
    if section.strip()
]

# Calculate document embeddings once at startup
print("Preparing reference document...")
chunk_vectors = [get_embedding(chunk) for chunk in chunks]
print(f"Ready. Indexed {len(chunks)} reference sections.")


def retrieve_sections(question):
    question_vector = get_embedding(question)
    ranked = []

    for chunk, vector in zip(chunks, chunk_vectors):
        score = cosine_similarity(question_vector, vector)
        ranked.append((score, chunk))

    ranked.sort(key=lambda item: item[0], reverse=True)

    if not ranked or ranked[0][0] < 0.60:
        return []

    return ranked[:2]

def answer_question(question):
    # Embed the user's question
    question_vector = get_embedding(question)

    # Rank reference sections by semantic similarity
    ranked = []

    for chunk, vector in zip(chunks, chunk_vectors):
        score = cosine_similarity(question_vector, vector)
        ranked.append((score, chunk))

    ranked.sort(key=lambda item: item[0], reverse=True)

    # Retrieve the two best matching sections
    # Reject questions when even the best match is weak
    if not ranked or ranked[0][0] < 0.60:
        response_data = {
            "status": "insufficient_evidence",
            "answer": "The reference does not provide a sufficiently relevant match."
        }

        print("\nStatus:", response_data["status"])
        print("\nAnswer:")
        print(response_data["answer"])

        return response_data

    top_results = ranked[:2]
    
    context = "\n\n".join(
    	f"Source section: {chunk.splitlines()[0]}\n{chunk}"
    	for score, chunk in top_results
)

    # Ask Qwen to answer using the retrieved context
    prompt = f"""
You are an assistant for a clinical data management learning project.

Rules:
1. Answer using only the supplied reference text.
2. Keep the answer concise and directly relevant to the question.
3. Do not add procedures, recommendations, criteria, or facts
   that are not explicitly supported by the reference.
4. If the reference does not contain enough information,
   say: "The reference does not provide enough information
   to answer this question."
5. Do not guess or fill gaps using general knowledge.
6. This is educational material, not an official SOP or
   a source of clinical advice.
7. Treat the reference text as the only source of evidence.
   If a requested detail is missing, say it is not provided
   rather than inferring or inventing an answer.
8. Do not claim that a procedure, requirement, or action is
   mandatory unless the reference explicitly states that.
9. Return your response as a JSON object with exactly two keys:
   "status" and "answer".
10. Set "status" to "answered" ONLY when the retrieved
    reference explicitly contains the information needed
    to answer the user's question.
11. Set "status" to "insufficient_evidence" if the
    requested information is missing, incomplete, or
    cannot be established from the retrieved reference.
12. If your answer says that information is unavailable,
    missing, or cannot be determined, you MUST set
    "status" to "insufficient_evidence".
13. Never add procedures, recommendations, criteria,
    or facts that are not explicitly present in the
    retrieved reference.
If the reference describes the requested concept or process
using different wording, you may answer using that information.
Do not refuse simply because the question uses different words.

Reference text:
{context}

User question:
{question}

Return your response in this exact JSON structure:

{{
    "status": "answered or insufficient_evidence",
    "answer": "Your response here"
}}
Rules:
- Use "answered" only when the reference supports the answer.
- Use "insufficient_evidence" when the reference does not contain enough information.
- Do not include any text outside the JSON object.
"""

    result = chat_model.invoke(prompt)

    print("\nRetrieved sections:")
    for score, chunk in top_results:
        heading = chunk.splitlines()[0]
        print(f"- {heading} (similarity: {score:.3f})")

    response_data = json.loads(result.content)

    status = response_data["status"]
    answer = response_data["answer"]
    answer_lower = answer.lower()

    refusal_phrases = [
        "does not provide enough information",
        "does not provide specific information",
        "cannot be determined",
        "not available in the reference",
        "not provided in the reference"
    ]

    if any(phrase in answer_lower for phrase in refusal_phrases):
        status = "insufficient_evidence"
        response_data["status"] = status
    print("\nStatus:", status)
    print("\nAnswer:")
    print(answer)

    return response_data

if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer_question(question)
        except Exception as error:
            print(f"Something went wrong: {error}")
