"""
Role 4 — Evaluator
Scores the review against established code-review criteria.
Outputs a numeric score and decides whether the pipeline should refine and retry.
"""

import llm
from models import Review, Evaluation
import config


SYSTEM_PROMPT = """\
You are a quality evaluator for code reviews. Given a code review, score it on a
scale of 0–10 and explain your reasoning.

Your output must follow this exact format:
SCORE: <number 0-10>
STRENGTHS:
- <bullet>
WEAKNESSES:
- <bullet>
REFINEMENT NEEDED: <yes/no>
REFINEMENT HINT: <one sentence of guidance for the prompt engineer, or "none">\
"""


def run(review: Review) -> Evaluation:
    """Score the review and return an Evaluation."""
    # TODO: call llm.call(user_prompt=review.content, system_prompt=SYSTEM_PROMPT)
    #       parse the structured output, set refinement_needed based on config.QUALITY_THRESHOLD
    raise NotImplementedError
