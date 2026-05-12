"""
Baseline: a generic LLM review with no specialization.
Used as the "before" measurement in the before/after comparison.
"""

import llm
from models import Review

GENERIC_SYSTEM_PROMPT = "You are a helpful assistant."


def run(code: str) -> Review:
    """Review `code` with no specialization — plain generic LLM."""
    # TODO: call llm.call with GENERIC_SYSTEM_PROMPT and a simple "please review this code" prompt
    raise NotImplementedError
