from semantic_rag import answer_question


test_cases = [
    {
        "question": "What is SAE reconciliation?",
        "should_answer": True,
        "expected_keywords": ["comparing", "discrepancies"]
    },
    {
        "question": "What does AE mean in a clinical trial?",
        "should_answer": True,
        "expected_keywords": ["adverse event"]
    },
    {
        "question": "What is the recommended dose of the study medication?",
        "should_answer": False,
        "expected_keywords": []
    },
    {
        "question": "Which databases are compared during SAE reconciliation?",
        "should_answer": True,
        "expected_keywords": ["clinical database", "safety database"]
    },
    {
        "question": "What is the recommended treatment duration?",
        "should_answer": False,
        "expected_keywords": []
    },
    {
        "question": "What is the incidence rate of serious adverse events in this study?",
        "should_answer": False,
        "expected_keywords": []
    },
    {
        "question": "What is a clinical data query?",
        "should_answer": True,
        "expected_keywords": ["clarify", "verify"]
    },
    {
        "question": "When may a clinical data query be raised?",
        "should_answer": True,
        "expected_keywords": ["missing", "inconsistent"]
    },
    {
        "question": "What is a pending query?",
        "should_answer": True,
        "expected_keywords": ["final resolution"]
    },
    {
        "question": "According to the reference, what is the resolution status of a pending query?",
        "should_answer": True,
        "expected_keywords": ["not yet"]
    },
    {
        "question": "What does an adverse event mean?",
        "should_answer": True,
        "expected_keywords": ["unfavorable", "medicinal product"]
    },
    {
        "question": "Does an adverse event necessarily have a causal relationship with treatment?",
        "should_answer": True,
        "expected_keywords": ["not necessarily"]
    },
    {
        "question": "What does SAE stand for?",
        "should_answer": True,
        "expected_keywords": ["serious adverse event"]
    },
    {
        "question": "What are examples of serious adverse event criteria?",
        "should_answer": True,
        "expected_keywords": ["death", "hospitalization"]
    },
    {
        "question": "What is the definition of a serious adverse event?",
        "should_answer": True,
        "expected_keywords": ["seriousness criteria"]
    },
    {
        "question": "What is database lock?",
        "should_answer": True,
        "expected_keywords": ["controlled milestone", "data cleaning"]
    },
    {
        "question": "When does database lock take place?",
        "should_answer": True,
        "expected_keywords": ["data cleaning", "review activities"]
    },
    {

   	"question": "Is this reference an official SOP or clinical guidance?",
    	"should_answer": False,
    	"expected_keywords": []
	
    },
    {
        "question": "Where should the exact SAE seriousness criteria be checked?",
        "should_answer": True,
        "expected_keywords": ["regulations", "study procedures"]
    },
    {

    	"question": "What determines the exact status definition of a pending query?",
    	"should_answer": True,
    	"expected_keywords": ["procedures", "system configuration"]

    },
    {
        "question": "What is the recommended medication for treating a serious adverse event?",
        "should_answer": False,
        "expected_keywords": []
    },
]


print("Answer quality evaluation:")

passed = 0

for test in test_cases:
    question = test["question"]
    expected = test["should_answer"]

    print("\nQuestion:", question)
    print("Expected to answer:", expected)

    response_data = answer_question(question)

    actual_status = response_data["status"]
    answer = response_data["answer"]
 
    actual_should_answer = actual_status == "answered"

    keywords = test["expected_keywords"]
    answer_lower = answer.lower()

    keywords_found = all(
        keyword.lower() in answer_lower
        for keyword in keywords
    )

if actual_should_answer == expected and (
    not expected or keywords_found
):
    print("PASS")
    passed += 1
else:
    print("FAIL")
    if actual_should_answer != expected:
        print("  Unexpected answer/refusal.")
    if expected and not keywords_found:
        missing_keywords = [
            keyword for keyword in keywords
            if keyword.lower() not in answer_lower
        ]
        print("  Missing keywords:", missing_keywords)