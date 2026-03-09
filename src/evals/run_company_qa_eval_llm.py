import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.server.mcp_server import answer_company_question_llm  # noqa: E402


EVAL_FILE = PROJECT_ROOT / "src" / "evals" / "cases" / "company_qa_eval_llm.json"
RESULTS_FILE = PROJECT_ROOT / "src" / "evals" / "results" / "company_qa_eval_results_llm.json"


def load_eval_cases() -> list:
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    return text.strip().lower()


def evaluate_case(case: dict) -> dict:
    company = case["company"]
    question = case["question"]
    actual_answer = answer_company_question_llm(company, question)
    actual_normalized = normalize_text(actual_answer)

    if "expected_answer" in case:
        expected = case["expected_answer"]
        passed = actual_normalized == normalize_text(expected)
        return {
            "id": case["id"],
            "company": company,
            "question": question,
            "passed": passed,
            "expected": expected,
            "actual": actual_answer,
            "check_type": "exact_match_normalized",
        }

    if "expected_answer_contains" in case:
        required_parts = case["expected_answer_contains"]
        missing_parts = [
            part for part in required_parts
            if normalize_text(part) not in actual_normalized
        ]
        passed = len(missing_parts) == 0
        return {
            "id": case["id"],
            "company": company,
            "question": question,
            "passed": passed,
            "expected_contains": required_parts,
            "missing_parts": missing_parts,
            "actual": actual_answer,
            "check_type": "contains_all_normalized",
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

    print("\n=== ChipScope-MCP LLM Company QA Eval Results ===\n")

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

        if "missing_parts" in result and result["missing_parts"]:
            print(f"  Missing parts: {result['missing_parts']}")

        print()

    print(f"Final Score: {passed_count}/{total_count} passed")
    save_results(results, passed_count, total_count)


if __name__ == "__main__":
    main()