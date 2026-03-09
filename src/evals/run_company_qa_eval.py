import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.server.mcp_server import answer_company_question  # noqa: E402


EVAL_FILE = PROJECT_ROOT / "src" / "evals" / "cases" / "company_qa_eval.json"
RESULTS_FILE = PROJECT_ROOT / "src" / "evals" / "results" / "company_qa_eval_results.json"


def load_eval_cases() -> list:
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_case(case: dict) -> dict:
    company = case["company"]
    question = case["question"]
    actual_answer = answer_company_question(company, question)

    if "expected_answer" in case:
        passed = actual_answer == case["expected_answer"]
        return {
            "id": case["id"],
            "company": company,
            "question": question,
            "passed": passed,
            "expected": case["expected_answer"],
            "actual": actual_answer,
            "check_type": "exact_match",
        }

    if "expected_answer_contains" in case:
        required_parts = case["expected_answer_contains"]
        passed = all(part in actual_answer for part in required_parts)
        return {
            "id": case["id"],
            "company": company,
            "question": question,
            "passed": passed,
            "expected_contains": required_parts,
            "actual": actual_answer,
            "check_type": "contains_all",
        }

    return {
        "id": case["id"],
        "company": company,
        "question": question,
        "passed": False,
        "actual": actual_answer,
        "check_type": "invalid_case",
    }


def save_results(results: list, passed_count: int, total_count: int) -> None:
    payload = {
        "summary": {
            "passed": passed_count,
            "total": total_count,
            "score": f"{passed_count}/{total_count}",
        },
        "results": results,
    }

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Saved results to: {RESULTS_FILE}")


def main() -> None:
    cases = load_eval_cases()
    results = [evaluate_case(case) for case in cases]

    passed_count = sum(result["passed"] for result in results)
    total_count = len(results)

    print("\n=== ChipScope-MCP Company QA Eval Results ===\n")

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {result['id']} - {result['question']}")
        print(f"  Company: {result['company']}")
        print(f"  Check type: {result['check_type']}")
        print(f"  Actual: {result['actual']}")

        if "expected" in result:
            print(f"  Expected: {result['expected']}")

        if "expected_contains" in result:
            print(f"  Expected contains: {result['expected_contains']}")

        print()

    print(f"Final Score: {passed_count}/{total_count} passed")
    save_results(results, passed_count, total_count)


if __name__ == "__main__":
    main()