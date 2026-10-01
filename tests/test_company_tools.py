from types import SimpleNamespace

import pytest

from src.server import mcp_server


def test_local_company_tools_return_structured_context():
    assert "lithography" in mcp_server.get_company_summary("ASML").lower()
    metadata = mcp_server.read_company_metadata("tsmc")
    assert metadata["country"] == "Taiwan"
    comparison = mcp_server.compare_companies("ASML", "TSMC")
    assert comparison["comparison"]["supply_chain_role"] == {
        "company_a": "Equipment supplier",
        "company_b": "Foundry",
    }


@pytest.mark.parametrize("company", ["../companies/asml", "..\\asml", "asml/../../secret", ""])
def test_company_name_cannot_read_arbitrary_paths(company):
    assert mcp_server.read_company_file(company).startswith("Invalid company name")
    assert "error" in mcp_server.read_company_metadata(company)
    assert mcp_server.answer_company_question(company, "Where is it based?").startswith("Invalid company name")


def test_baseline_answers_and_unknown_company():
    assert mcp_server.answer_company_question("asml", "Where is ASML based?") == "ASML is based in Netherlands."
    assert "Equipment supplier" in mcp_server.answer_company_question("asml", "What is its role?")
    assert "Lithography systems" in mcp_server.answer_company_question("asml", "What is it known for?")
    assert "Semiconductor equipment" in mcp_server.answer_company_question("asml", "What does ASML do?")
    assert mcp_server.answer_company_question("amd", "Where is AMD based?") == "No local company file found for 'amd'."


def test_llm_tool_uses_local_context_and_handles_missing_key(monkeypatch):
    monkeypatch.setattr(mcp_server, "client", None)
    assert "OPENAI_API_KEY" in mcp_server.answer_company_question_llm("asml", "What is it known for?")

    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(output_text="  ASML makes lithography systems.  ")

    monkeypatch.setattr(mcp_server, "client", SimpleNamespace(responses=SimpleNamespace(create=fake_create)))
    assert mcp_server.answer_company_question_llm("asml", "What is it known for?") == "ASML makes lithography systems."
    assert "Lithography systems, especially EUV" in captured["input"]
    assert captured["model"] == mcp_server.OPENAI_MODEL
    assert mcp_server.answer_company_question_llm("../bad", "question").startswith("Invalid company name")
