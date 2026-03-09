import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from openai import OpenAI

load_dotenv()

mcp = FastMCP("ChipScope-MCP")

BASE_DIR = Path(__file__).resolve().parent.parent
COMPANIES_DIR = BASE_DIR / "data" / "raw" / "companies"
METADATA_DIR = BASE_DIR / "data" / "processed" / "company_metadata"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def read_company_file(company: str) -> str:
    filename = f"{company.strip().lower()}.txt"
    filepath = COMPANIES_DIR / filename

    if not filepath.exists():
        return f"No local company file found for '{company}'."

    return filepath.read_text(encoding="utf-8")


def read_company_metadata(company: str) -> dict:
    filename = f"{company.strip().lower()}.json"
    filepath = METADATA_DIR / filename

    if not filepath.exists():
        return {"error": f"No metadata file found for '{company}'."}

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@mcp.tool()
def get_company_summary(company: str) -> str:
    return read_company_file(company)


@mcp.tool()
def compare_companies(company_a: str, company_b: str) -> dict:
    data_a = read_company_metadata(company_a)
    data_b = read_company_metadata(company_b)

    if "error" in data_a:
        return data_a
    if "error" in data_b:
        return data_b

    return {
        "company_a": data_a["company"],
        "company_b": data_b["company"],
        "comparison": {
            "country": {
                "company_a": data_a["country"],
                "company_b": data_b["country"]
            },
            "segment": {
                "company_a": data_a["segment"],
                "company_b": data_b["segment"]
            },
            "specialization": {
                "company_a": data_a["specialization"],
                "company_b": data_b["specialization"]
            },
            "supply_chain_role": {
                "company_a": data_a["supply_chain_role"],
                "company_b": data_b["supply_chain_role"]
            }
        }
    }


@mcp.tool()
def answer_company_question(company: str, question: str) -> str:
    note = read_company_file(company)
    metadata = read_company_metadata(company)

    if note.startswith("No local company file found"):
        return note

    if "error" in metadata:
        return metadata["error"]

    question_lower = question.strip().lower()

    if "where" in question_lower or "country" in question_lower or "based" in question_lower:
        return f"{metadata['company']} is based in {metadata['country']}."

    if "role" in question_lower or "supply chain" in question_lower:
        return (
            f"{metadata['company']} plays the role of "
            f"{metadata['supply_chain_role']} in the semiconductor supply chain."
        )

    if "special" in question_lower or "known for" in question_lower:
        return (
            f"{metadata['company']} is especially known for "
            f"{metadata['specialization']}."
        )

    if "segment" in question_lower or "what does" in question_lower:
        return (
            f"{metadata['company']} operates in {metadata['segment']}. "
            f"{note}"
        )

    return (
        f"{metadata['company']} is a semiconductor company based in "
        f"{metadata['country']}. It operates in {metadata['segment']} and is "
        f"known for {metadata['specialization']}. "
        f"Supply chain role: {metadata['supply_chain_role']}. "
        f"Additional note: {note}"
    )


@mcp.tool()
def answer_company_question_llm(company: str, question: str) -> str:
    note = read_company_file(company)
    metadata = read_company_metadata(company)

    if note.startswith("No local company file found"):
        return note

    if "error" in metadata:
        return metadata["error"]

    if client is None:
        return "OPENAI_API_KEY is not set in the .env file."

    prompt = f"""
You are a semiconductor research assistant.

Answer the user's question using only the provided company metadata and company note.
Do not invent facts.
Be concise and grounded.

Very important:
- Use the exact company name.
- Prefer the exact metadata wording when relevant.
- If the user asks about role or supply chain, explicitly use the phrase "semiconductor supply chain".
- If the user asks a broad question like "Tell me about X" or "Summarize X", format the answer as a short paragraph that explicitly includes:
  - company name
  - country using the exact country value from metadata
  - segment using the exact segment value from metadata
  - specialization using the exact specialization value from metadata
  - supply chain role using the exact supply_chain_role value from metadata

Do not replace the country with an adjective like "Dutch" or "American" when the metadata gives a country name.
If the answer cannot be supported by the provided context, say so clearly.

Company metadata:
{json.dumps(metadata, indent=2)}

Company note:
{note}

User question:
{question}

Return only the answer text.
""".strip()

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    return response.output_text.strip()


@mcp.resource("semiconductor://intro")
def semiconductor_intro() -> str:
    return (
        "ChipScope-MCP is an MCP-native Semiconductor Intelligence Agent. "
        "This version reads local semiconductor company notes from files and exposes them through MCP."
    )


@mcp.resource("semiconductor://company/{company}")
def company_resource(company: str) -> str:
    return read_company_file(company)


if __name__ == "__main__":
    mcp.run()