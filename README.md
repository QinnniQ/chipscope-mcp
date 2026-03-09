![ChipScope-MCP Banner](assets/chipscope-mcp-banner.png)

# ChipScope-MCP

ChipScope-MCP is an MCP-native Semiconductor Intelligence Agent built to explore how modern AI systems can combine domain-specific context, tool-based interfaces, and evaluation-driven iteration.

It answers semiconductor company questions using local company notes, structured metadata, a deterministic baseline QA system, and an LLM-backed QA tool.

## Why this project matters

Many AI portfolio projects stop at a chatbot demo.

ChipScope-MCP goes further by combining:
- **MCP (Model Context Protocol)** for tool and resource exposure
- a focused, high-value domain: **semiconductor intelligence**
- both **deterministic** and **LLM-based** question answering
- **repeatable evals** used to measure and improve system behavior

The goal is to demonstrate practical AI engineering skills that matter for modern agent systems: structured context design, grounded generation, evaluation workflows, and iterative improvement.

## What it does

ChipScope-MCP currently supports:
- MCP tools for semiconductor company summaries and comparisons
- MCP resources and resource templates for company-specific notes
- deterministic company QA as a controlled baseline
- LLM-backed company QA grounded on local metadata and notes
- saved baseline and LLM eval runs
- side-by-side eval comparison for system analysis

## Current companies

The current local dataset includes:
- ASML
- TSMC
- Intel

## Tech stack

- Python
- MCP Python SDK
- OpenAI API
- PowerShell
- JSON-based eval datasets

## Project structure

```text
chipscope-mcp/
│
├── assets/
├── docs/
├── notebooks/
├── src/
│   ├── data/
│   │   ├── raw/
│   │   │   └── companies/
│   │   │       ├── asml.txt
│   │   │       ├── tsmc.txt
│   │   │       └── intel.txt
│   │   └── processed/
│   │       └── company_metadata/
│   │           ├── asml.json
│   │           ├── tsmc.json
│   │           └── intel.json
│   ├── evals/
│   │   ├── cases/
│   │   ├── results/
│   │   ├── compare_eval_runs.py
│   │   ├── run_company_qa_eval.py
│   │   └── run_company_qa_eval_llm.py
│   └── server/
│       └── mcp_server.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Architecture

ChipScope-MCP is organized around a simple but extensible agent architecture:

1. **Local semiconductor data layer**
   - company notes stored as raw text files
   - company metadata stored as structured JSON

2. **MCP server layer**
   - exposes tools for summaries, comparison, and question answering
   - exposes resources and resource templates for semiconductor company context

3. **QA layer**
   - a deterministic baseline QA tool for controlled behavior
   - an LLM-backed QA tool for more flexible grounded responses

4. **Evaluation layer**
   - baseline eval cases for deterministic QA
   - LLM-specific eval cases for generative QA
   - saved result artifacts for comparison and iteration

## System flow

```text
Local company notes + metadata
            ↓
        MCP server
            ↓
   Tools / Resources / Templates
            ↓
 Baseline QA tool   |   LLM QA tool
            ↓
      Eval runners + saved results
```

## Why MCP and evals

This project was intentionally built around two ideas that are becoming increasingly important in modern AI engineering:

### Why MCP
MCP helps standardize how AI systems expose and consume:
- tools
- resources
- structured context

Instead of building a one-off chatbot, ChipScope-MCP is designed like a small agent system with explicit interfaces for company summaries, company resources, comparisons, and question answering.

### Why evals
AI systems are easy to demo and much harder to measure.

ChipScope-MCP includes:
- a deterministic baseline QA system
- an LLM-backed QA system
- repeatable eval datasets
- saved eval artifacts
- iterative improvement based on failure analysis

This makes the project less about prompting in isolation and more about building AI systems that can be tested, compared, and improved over time.

## What this demonstrates

This project demonstrates practical skills in:

- MCP-native tool and resource design
- structured and unstructured context handling
- deterministic vs LLM-based system comparison
- evaluation-driven development
- prompt refinement based on measured failure cases
- building domain-specific AI systems rather than generic demos

From a portfolio perspective, ChipScope-MCP is meant to show how modern AI engineering goes beyond model calls alone and includes interfaces, grounding, testing, and iteration.

## Roadmap

Planned next improvements:

- ingest real semiconductor filings and earnings transcripts
- add retrieval with evidence-backed answers
- attach citations or source snippets to answers
- expand the evaluation suite beyond simple QA checks
- add a lightweight UI for interactive exploration
- benchmark baseline vs LLM behavior on larger domain tasks

## Core components

### MCP server
The MCP server exposes:
- tools
- resources
- resource templates

Main server file:
```text
src/server/mcp_server.py
```

### Baseline QA
A deterministic semiconductor QA tool used as a controlled baseline.

### LLM QA
An LLM-backed semiconductor QA tool grounded on local company metadata and notes.

### Evals
The project includes:
- a baseline eval suite
- an LLM eval suite
- saved JSON eval results
- an eval comparison script

## Example capabilities

Example questions:
- Where is ASML based?
- What is TSMC known for?
- What role does Intel play in the semiconductor supply chain?
- Tell me about ASML.

## Eval results

Current status:
- Baseline QA eval: **5/5**
- LLM QA eval: **5/5**

This score was achieved through iterative prompt refinement and evaluation-driven debugging.

## What I learned

This project helped me practice:
- MCP server design
- tool vs resource separation
- structured vs unstructured context handling
- deterministic vs LLM system comparison
- evaluation-driven iteration
- prompt refinement based on failure analysis

## Setup

Clone the repository and create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file with your OpenAI settings:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

## How to run

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the baseline eval:

```powershell
python .\src\evals\run_company_qa_eval.py
```

Run the LLM eval:

```powershell
python .\src\evals\run_company_qa_eval_llm.py
```

Compare eval runs:

```powershell
python .\src\evals\compare_eval_runs.py
```

Launch the MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector
```

Then connect it to:

- Command:
```text
C:/Users/YOUR_NAME/Documents/chipscope-mcp/.venv/Scripts/python.exe
```

- Arguments:
```text
src/server/mcp_server.py
```

## Project blurbs

### GitHub repo short description
MCP-native semiconductor intelligence agent with deterministic and LLM-based QA, structured metadata, and eval-driven iteration.

### LinkedIn / CV project blurb
Built ChipScope-MCP, an MCP-native Semiconductor Intelligence Agent that combines structured company metadata, local context resources, deterministic and LLM-based QA tools, and repeatable eval workflows. Designed to demonstrate modern AI engineering skills in tool/resource design, grounded generation, and evaluation-driven iteration.

### Recruiter-facing version
Built an MCP-native semiconductor intelligence system with baseline and LLM-backed QA, structured context handling, and eval-driven prompt refinement, showcasing practical AI engineering beyond a standard chatbot demo.

## Next steps

Planned improvements:
- ingest real semiconductor filings and earnings transcripts
- add citation-style evidence retrieval
- expand the eval set
- add a simple UI
- add benchmark-style reporting for answer quality

## Author

Nicholai Gay  
AI Engineer focused on MCP, agent systems, evaluation, and domain-specific AI tooling.
