"""
Role 2 — Prompt Engineer
Takes a ScoutOutput and writes an optimized system prompt for a code review agent.
"""

import dataclasses
import json
import llm
from models import ScoutOutput, GeneratedPrompt

AVAILABLE_TOOLS = ["grep", "linter", "security_scanner", "style_checker", "complexity_analyzer"]

SYSTEM_PROMPT = f"""\
You are an expert prompt engineer. You will receive a specialization spec — a JSON object
describing a code sample's language, key risks, focus areas, and the ideal reviewer persona.

Your job: write a system prompt that turns a general-purpose LLM into that reviewer.
The system prompt you write must:
- Embody the reviewer persona described in the spec
- Prioritize the risks listed as the most important things to catch
- Use the focus areas as its explicit evaluation criteria

Also select the tools the reviewer should use from this list:
{AVAILABLE_TOOLS}
Only pick tools that are relevant to the language and risks in the spec.

Respond with a single JSON object — no markdown, no explanation, just the object:
{{
  "system_prompt": "<the full system prompt text>",
  "selected_tools": ["<tool>", ...]
}}\
"""


def run(scout_output: ScoutOutput) -> GeneratedPrompt:
    """Write a system prompt and pick tools based on the scout's specialization spec."""
    user_prompt = json.dumps(dataclasses.asdict(scout_output), indent=2)

    raw = llm.call(user_prompt, system_prompt=SYSTEM_PROMPT, temperature=0.4)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        stripped = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(stripped)

    selected = [t for t in data.get("selected_tools", []) if t in AVAILABLE_TOOLS]

    return GeneratedPrompt(
        system_prompt=data.get("system_prompt", ""),
        selected_tools=selected,
        raw=raw,
    )
