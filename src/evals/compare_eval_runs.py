import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

BASELINE_RESULTS_FILE = PROJECT_ROOT / "src" / "evals" / "results" / "company_qa_eval_results.json"
LLM_RESULTS_FILE = PROJECT_ROOT / "src" / "evals" / "results" / "company_qa_eval_results_llm.json"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_result_map(results: list) -> dict:
    paired = {}
    for item in results:
        key = (item["company"].strip().casefold(), item["question"].strip().casefold())
        if key in paired:
            raise ValueError(f"Duplicate evaluation case: {key}")
        paired[key] = item
    return paired


def main() -> None:
    baseline = load_json(BASELINE_RESULTS_FILE)
    llm = load_json(LLM_RESULTS_FILE)

    baseline_results = build_result_map(baseline["results"])
    llm_results = build_result_map(llm["results"])

    print("\n=== ChipScope-MCP Eval Comparison ===\n")
    print(f"Baseline score: {baseline['summary']['score']}")
    print(f"LLM score:      {llm['summary']['score']}\n")

    all_cases = sorted(set(baseline_results) | set(llm_results))

    for company, question in all_cases:
        base_case = baseline_results.get((company, question))
        llm_case = llm_results.get((company, question))

        print(f"Case: {company} - {question}")

        if base_case:
            print(f"  Baseline passed: {base_case['passed']}")
            print(f"  Baseline actual: {base_case['actual']}")

        if llm_case:
            print(f"  LLM passed:      {llm_case['passed']}")
            print(f"  LLM actual:      {llm_case['actual']}")

        print()


if __name__ == "__main__":
    main()
