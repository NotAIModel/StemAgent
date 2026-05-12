"""
Role 3 — Executor
Uses the system prompt produced by the prompt engineer to actually review code.
This is the "specialized" review — the payoff of the self-specialization pipeline.
"""

import llm
from models import GeneratedPrompt, Review


def run(code: str, generated_prompt: GeneratedPrompt) -> Review:
    """Review `code` using the generated system prompt."""
    # TODO: call llm.call(user_prompt=code, system_prompt=generated_prompt.system_prompt)
    #       and wrap result in a Review
    raise NotImplementedError
