from semantic_rag import (
    chunks,
    chunk_vectors,
    get_embedding,
    cosine_similarity
)

# Test questions and their expected reference sections
test_questions = [
    {
        "question": "What is SAE reconciliation?",
        "expected_section": "SAE Reconciliation"
    },
    {
        "question": "How do we cross-check serious safety cases between systems?",
        "expected_section": "SAE Reconciliation"
    },
    {
        "question": "What does AE mean in a clinical trial?",
        "expected_section": "Adverse Event (AE)"
    },
    {
        "question": "What is the recommended dose of the study medication?",
        "expected_section": None
    }
]

# Configurations to compare
thresholds = [0.50, 0.60, 0.70]
top_k_values = [1, 2, 3]


def retrieve_with_settings(question, threshold, top_k):

    question_vector = get_embedding(question)

    ranked = []

    for chunk, vector in zip(chunks, chunk_vectors):
        score = cosine_similarity(question_vector, vector)
        ranked.append((score, chunk))

    ranked.sort(key=lambda item: item[0], reverse=True)

    if not ranked or ranked[0][0] < threshold:
        return []

    return [
        item for item in ranked[:top_k]
        if item[0] >= threshold
    ]


print("\nRETRIEVAL CONFIGURATION EXPERIMENT")
print("=" * 55)

for threshold in thresholds:

    for top_k in top_k_values:

        passed = 0

        for test in test_questions:

            question = test["question"]
            expected = test["expected_section"]

            results = retrieve_with_settings(
                question, threshold, top_k
            )

            if expected is None:
                success = len(results) == 0
            else:
                success = any(
                    expected.lower() in chunk.lower()
                    for score, chunk in results
                )

            if success:
                passed += 1

        accuracy = passed / len(test_questions) * 100

        print(
            f"Threshold: {threshold:.2f} | "
            f"Top K: {top_k} | "
            f"Passed: {passed}/{len(test_questions)} | "
            f"Score: {accuracy:.1f}%"
        )