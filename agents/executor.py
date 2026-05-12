"""
Role 3 — Executor
Uses the system prompt from the prompt engineer to perform the actual code review.
This is the specialized review — the payoff of the self-specialization pipeline.
"""

import json
import llm
from models import GeneratedPrompt, Review


def run(code: str, generated_prompt: GeneratedPrompt) -> Review:
    """Review `code` using the generated system prompt."""
    tools_note = ", ".join(generated_prompt.selected_tools) if generated_prompt.selected_tools else "none"
    user_prompt = (
        f"Review the following code:\n\n{code}\n\n"
        f"Also note these tools are available to you: {tools_note}"
    )

    # Append output schema to whatever the prompt engineer wrote so the response
    # is always parseable regardless of how the system prompt was phrased.
    system_prompt = generated_prompt.system_prompt + "\n\n" + (
        "Respond with a single JSON object — no markdown, no explanation:\n"
        "{\n"
        '  "comments": ["<finding>", ...],\n'
        '  "severity_counts": {"high": <n>, "medium": <n>, "low": <n>},\n'
        '  "summary": "<one-paragraph overall assessment>"\n'
        "}"
    )

    raw = llm.call(user_prompt, system_prompt=system_prompt, temperature=0.3)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        stripped = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(stripped)

    counts = data.get("severity_counts", {})
    severity_counts = {
        "high":   int(counts.get("high", 0)),
        "medium": int(counts.get("medium", 0)),
        "low":    int(counts.get("low", 0)),
    }

    return Review(
        comments=data.get("comments", []),
        severity_counts=severity_counts,
        summary=data.get("summary", ""),
        raw=raw,
    )
