"""
Role 4 — Evaluator
Scores the review for thoroughness and accuracy. Sets needs_refinement when
the score falls below config.QUALITY_THRESHOLD.
"""

import dataclasses
import json
import llm
import config
from models import Review, Evaluation


SYSTEM_PROMPT = """\
You are a senior software engineer evaluating a code review for thoroughness and accuracy.

You will receive a code review as JSON. Score it on a scale of 0–10 based on:
- Did it catch all meaningful issues?
- Are the severity assignments accurate?
- Is the summary clear and actionable?

Respond with a single JSON object — no markdown, no explanation, just the object:
{
  "score": <number 0.0–10.0>,
  "reasoning": "<one paragraph explaining the score>"
}\
"""


def run(review: Review) -> Evaluation:
    """Score `review` and return an Evaluation."""
    user_prompt = json.dumps(dataclasses.asdict(review), indent=2)

    raw = llm.call(user_prompt, system_prompt=SYSTEM_PROMPT, temperature=0.3)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        stripped = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(stripped)

    score = float(data.get("score", 0.0))

    return Evaluation(
        score=score,
        reasoning=data.get("reasoning", ""),
        needs_refinement=score < config.QUALITY_THRESHOLD,
        raw=raw,
    )
