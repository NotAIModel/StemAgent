# Baseline: generic review with no specialization — used for before/after comparison

import json
import llm
from models import Review

SYSTEM_PROMPT = "You are a code reviewer. Review the following code and identify issues."

OUTPUT_SCHEMA = (
    "\n\nRespond with a single JSON object — no markdown, no explanation, just the object:\n"
    "{\n"
    '  "comments": ["<finding>", ...],\n'
    '  "severity_counts": {"high": <n>, "medium": <n>, "low": <n>},\n'
    '  "summary": "<one-paragraph overall assessment>"\n'
    "}"
)


def run(code: str) -> Review:
    raw = llm.call(
        user_prompt=code,
        system_prompt=SYSTEM_PROMPT + OUTPUT_SCHEMA,
        temperature=0.3,
    )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        stripped = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(stripped)

    counts = data.get("severity_counts", {})
    return Review(
        comments=data.get("comments", []),
        severity_counts={
            "high":   int(counts.get("high", 0)),
            "medium": int(counts.get("medium", 0)),
            "low":    int(counts.get("low", 0)),
        },
        summary=data.get("summary", ""),
        raw=raw,
    )
