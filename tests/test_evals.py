import pytest

from src.evals import compare_eval_runs, run_company_qa_eval, run_company_qa_eval_llm


def test_baseline_suite_matches_its_five_saved_cases():
    cases = run_company_qa_eval.load_eval_cases()
    assert len(cases) == 5
    assert all(run_company_qa_eval.evaluate_case(case)["passed"] for case in cases)


def test_llm_eval_check_is_only_string_matching(monkeypatch):
    monkeypatch.setattr(run_company_qa_eval_llm, "answer_company_question_llm", lambda company, question: "ASML is in the Netherlands.")
    case = {"id": "sample", "company": "asml", "question": "Where?", "expected_answer_contains": ["ASML", "Netherlands"]}
    result = run_company_qa_eval_llm.evaluate_case(case)
    assert result["passed"] is True
    assert result["check_type"] == "contains_all_normalized"
    assert run_company_qa_eval_llm.evaluate_case({**case, "expected_answer_contains": ["TSMC"]})["passed"] is False


def test_comparison_pairs_same_questions_despite_different_ids(capsys):
    baseline = compare_eval_runs.load_json(compare_eval_runs.BASELINE_RESULTS_FILE)
    llm = compare_eval_runs.load_json(compare_eval_runs.LLM_RESULTS_FILE)
    baseline_map = compare_eval_runs.build_result_map(baseline["results"])
    llm_map = compare_eval_runs.build_result_map(llm["results"])
    assert len(baseline_map) == len(llm_map) == len(set(baseline_map) & set(llm_map)) == 5

    compare_eval_runs.main()
    output = capsys.readouterr().out
    assert output.count("Case:") == 5
    assert output.count("Baseline passed:") == 5
    assert output.count("LLM passed:") == 5


def test_duplicate_eval_questions_are_rejected():
    row = {"id": "1", "company": "ASML", "question": "Where?", "passed": True, "actual": "Netherlands"}
    with pytest.raises(ValueError, match="Duplicate evaluation case"):
        compare_eval_runs.build_result_map([row, {**row, "id": "2"}])
