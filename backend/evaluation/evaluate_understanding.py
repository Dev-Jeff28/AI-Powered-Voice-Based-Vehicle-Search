import json
from pathlib import Path

from app.clients.openrouter_client import OpenRouterClient
from app.clients.gemini_client import GeminiClient
from app.services.understanding import UnderstandingService


FIELDS = [
    "brand",
    "model",
    "year",
    "usage",
    "price",
    "city",
    "body_type",
    "fuel_type"
]


def normalize(value):
    if isinstance(value, str):
        return value.strip().lower()

    return value


def values_match(expected, actual):
    return normalize(expected) == normalize(actual)


def load_test_cases():
    path = (
        Path(__file__).parent
        / "understanding_cases.json"
    )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate():
    test_cases = load_test_cases()

    llm_client = GeminiClient()  # Use GeminiClient for evaluation.

    # SearchService is not required by understand_query().
    understanding_service = UnderstandingService(
        llm_client,
        None
    )

    total_cases = len(test_cases)
    correct_cases = 0

    field_correct = {
        field: 0
        for field in FIELDS
    }

    field_total = {
        field: 0
        for field in FIELDS
    }

    print()
    print("=" * 70)
    print("UNDERSTANDING SERVICE EVALUATION")
    print("=" * 70)
    print()

    for index, test_case in enumerate(
        test_cases,
        start=1
    ):

        query = test_case["query"]
        expected = test_case["expected"]

        print(f"Test {index}/{total_cases}")
        print(f"Query: {query}")

        try:
            actual_query = (
                understanding_service.understand_query(
                    query
                )
            )

            actual = actual_query.model_dump()

            case_correct = True

            for field in FIELDS:

                expected_value = expected.get(field)
                actual_value = actual.get(field)

                # Count every field for exact-query evaluation.
                field_total[field] += 1

                if values_match(
                    expected_value,
                    actual_value
                ):
                    field_correct[field] += 1

                else:
                    case_correct = False

            if case_correct:
                correct_cases += 1
                print("Result: PASS ✓")

            else:
                print("Result: FAIL ✗")

                print()
                print("Expected:")
                print(
                    json.dumps(
                        expected,
                        indent=2
                    )
                )

                print()
                print("Actual:")
                print(
                    json.dumps(
                        actual,
                        indent=2
                    )
                )

        except Exception as error:

            print("Result: ERROR ✗")
            print(f"Error: {error}")

        print("-" * 70)

    exact_accuracy = (
        correct_cases / total_cases * 100
        if total_cases > 0
        else 0
    )

    total_fields_correct = sum(
        field_correct.values()
    )

    total_fields = sum(
        field_total.values()
    )

    field_accuracy = (
        total_fields_correct / total_fields * 100
        if total_fields > 0
        else 0
    )

    print()
    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print(
        f"Total queries:        {total_cases}"
    )

    print(
        f"Correct queries:      {correct_cases}"
    )

    print(
        f"Incorrect queries:    "
        f"{total_cases - correct_cases}"
    )

    print(
        f"Exact query accuracy: "
        f"{exact_accuracy:.2f}%"
    )

    print(
        f"Field accuracy:       "
        f"{field_accuracy:.2f}%"
    )

    print()
    print("FIELD ACCURACY")
    print("-" * 70)

    for field in FIELDS:

        accuracy = (
            field_correct[field]
            / field_total[field]
            * 100
            if field_total[field] > 0
            else 0
        )

        print(
            f"{field:<15} "
            f"{field_correct[field]}/"
            f"{field_total[field]} "
            f"({accuracy:.2f}%)"
        )

    print("=" * 70)


if __name__ == "__main__":
    evaluate()