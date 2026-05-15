# Stem Agent

A four-stage LLM pipeline for code review: Scout infers language and risks from the source, Prompt Engineer builds a tailored system prompt, Executor runs the review, and Evaluator scores it and can trigger refinement. The same pipeline adapts to different languages and codebases without hardcoded rules.

## Setup

```bash
git clone <repo-url>
cd StemAgent
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
```

Default provider is Groq (`llama-3.3-70b-versatile`). Set `PROVIDER=openai` to use OpenAI (`gpt-4o-mini`).

## Run

```bash
python main.py samples/sample.py
python main.py samples/sample.cpp
```

Prints scout output, generated system prompt, review findings, and evaluation score. Defaults to `samples/sample.py` if no path is given.

## Experiments

Run from the project root with the venv active:

| Script | What it shows |
|--------|----------------|
| `python experiments/before_after.py` | Side-by-side baseline vs full stem pipeline on `samples/sample.py`, with a delta of findings. |
| `python experiments/compare_specialization.py` | Scout specs for Python (`sample.py`) vs C++ (`sample.cpp`) to show environment-driven specialization. |
| `python experiments/cross_model.py` | Groq vs OpenAI × baseline vs stem agent across two samples (5 runs each); writes `experiments/results_cross_model.md`. |

## Tests

```bash
pytest tests/ -v
```

Unit tests mock LLM calls. Integration tests in `test_pipeline_integration.py` hit the live API when run.

## Project structure

```
StemAgent/
├── main.py                 # CLI: read file, run pipeline, print results
├── pipeline.py             # Orchestrates agents and refinement loop
├── baseline.py             # Generic reviewer (no scout/prompt engineer)
├── config.py               # Provider, API keys, model names, thresholds
├── llm.py                  # Groq/OpenAI call wrapper
├── models.py               # ScoutOutput, GeneratedPrompt, Review, Evaluation
├── agents/
│   ├── scout.py            # Infers language, focus areas, risks from code
│   ├── prompt_engineer.py  # Builds system prompt and tool list from scout spec
│   ├── executor.py         # Runs code review with generated prompt
│   └── evaluator.py        # Scores review quality (0–10), flags refinement
├── samples/
│   ├── sample.py           # Python sample with planted issues
│   ├── sample.cpp          # C++ sample with planted issues
│   ├── sample_advanced.py
│   └── sample_advanced_clean.py
├── experiments/            # Comparison and benchmarking scripts
└── tests/                  # pytest suite per agent and pipeline
```
