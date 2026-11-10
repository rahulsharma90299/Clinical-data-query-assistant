
import semantic_rag as rag

# Test questions and their expected relevant sections
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


def run_experiment(threshold, top_k):

    precisions = []
    recalls = []
    correct_abstentions = 0
    unanswered_questions = 0

    for test in test_questions:

        question = test["question"]
        expected = test["expected_section"]

        question_vector = rag.get_embedding(question)

        ranked = []

        for chunk, vector in zip(rag.chunks, rag.chunk_vectors):
            score = rag.cosine_similarity(question_vector, vector)
            ranked.append((score, chunk))

        ranked.sort(key=lambda item: item[0], reverse=True)

        if not ranked or ranked[0][0] < threshold:
            results = []
        else:
            results = ranked[:top_k]

        retrieved_sections = [
            chunk.splitlines()[0] for score, chunk in results
        ]

        if expected is None:
            unanswered_questions += 1

            if not results:
                correct_abstentions += 1

            continue

        relevant_found = sum(
            1 for section in retrieved_sections
            if expected.lower() in section.lower()
        )

        precision = relevant_found / len(results) if results else 0
        recall = 1 if relevant_found > 0 else 0

        precisions.append(precision)
        recalls.append(recall)

    avg_precision = sum(precisions) / len(precisions)
    avg_recall = sum(recalls) / len(recalls)

    abstention_accuracy = (
        correct_abstentions / unanswered_questions
        if unanswered_questions else 0
    )

    return avg_precision, avg_recall, abstention_accuracy


print("\nRETRIEVAL CONFIGURATION EXPERIMENT")
print("-" * 65)

print(
    f"{'Threshold':<12}"
    f"{'Top K':<10}"
    f"{'Precision':<14}"
    f"{'Recall':<12}"
    f"{'Abstention':<12}"
)

print("-" * 65)

for threshold in thresholds:
    for top_k in top_k_values:

        precision, recall, abstention = run_experiment(
            threshold, top_k
        )

        print(
            f"{threshold:<12.2f}"
            f"{top_k:<10}"
            f"{precision:<14.3f}"
            f"{recall:<12.3f}"
            f"{abstention:<12.3f}"
        )

print("-" * 65)

