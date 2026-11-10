
from semantic_rag import retrieve_sections

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

passed = 0

for test in test_questions:
    question = test["question"]
    expected = test["expected_section"]

    results = retrieve_sections(question)

    if expected is None:
        success = len(results) == 0
    else:
        success = any(
            expected.lower() in chunk.lower()
            for score, chunk in results
        )

    status = "PASS" if success else "FAIL"
    print(f"{status} | {question}")

    if results:
        print(f"  Best similarity: {results[0][0]:.3f}")
        print(f"  Best match: {results[0][1].splitlines()[0]}")

    if success:
        passed += 1

print(f"\nResults: {passed}/{len(test_questions)} tests passed")
