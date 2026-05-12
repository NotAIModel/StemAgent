# Stem Agent — Project Context

## Architecture
Single LLM (Groq, llama-3.3-70b-versatile), four sequential roles:
1. Scout — analyzes raw code, outputs a `ScoutOutput` JSON spec
2. Prompt Engineer — takes spec, writes system prompt + rationale
3. Executor — runs code review using the generated system prompt
4. Evaluator — scores review 0–10, triggers refinement if below threshold

## Agent interfaces

### Scout (`agents/scout.py`)
- **Input:** `code: str` — raw source code, no assumptions about language or domain
- **Output:** `ScoutOutput` dataclass
  ```json
  {
    "language": "<language>",
    "focus_areas": ["<area>", ...],
    "risks": ["<concrete risk found in this code>", ...],
    "reviewer_persona": "<one-sentence description of ideal reviewer>"
  }
  ```
- **LLM call:** `temperature=0.3` (low — deterministic analysis)
- **JSON parsing:** strips accidental markdown fences before parsing

## Rules
- All inter-agent communication in JSON
- No LangChain or agent frameworks — raw API calls only
- Every agent has one job, one file
- `ScoutOutput` is inferred entirely from the code — nothing hardcoded