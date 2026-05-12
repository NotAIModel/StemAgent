"""
Role 1 — Scout
Analyzes raw code and returns a structured specialization spec.
No task-specific knowledge is hard-coded; the LLM infers everything from the code.
"""

import json
import llm
from models import ScoutOutput


SYSTEM_PROMPT = """\
You are a code analysis expert. Given a code snippet, analyze it and respond with
a single JSON object — no markdown, no explanation, just the object.

Schema:
{
  "language": "<programming language>",
  "focus_areas": ["<area>", ...],
  "risks": ["<concrete risk found in this code>", ...],
  "reviewer_persona": "<description of the ideal reviewer for this code>"
}

focus_areas: the review dimensions most relevant to this code
  (e.g. "security", "error handling", "performance", "readability", "correctness").
risks: specific issues or patterns in the code that a reviewer must catch
  (e.g. "SQL injection via f-string interpolation in get_user()").
reviewer_persona: one sentence describing the specialist best suited to review it.\
"""


def run(code: str) -> ScoutOutput:
    """Analyze `code` and return a ScoutOutput inferred entirely from it."""
    user_prompt = f"Analyze this code:\n\n```\n{code}\n```"

    raw = llm.call(user_prompt, system_prompt=SYSTEM_PROMPT, temperature=0.3)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Strip accidental markdown fences if the model wrapped its output
        stripped = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(stripped)

    return ScoutOutput(
        language=data.get("language", ""),
        focus_areas=data.get("focus_areas", []),
        risks=data.get("risks", []),
        reviewer_persona=data.get("reviewer_persona", ""),
        raw=raw,
    )
