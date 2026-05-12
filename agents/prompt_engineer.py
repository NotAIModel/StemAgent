"""
Role 2 — Prompt Engineer
Takes the scout's structured summary and writes an optimized system prompt
for a code review agent. Can be called again with a refinement hint.
"""

import llm
from models import ScoutOutput, GeneratedPrompt


SYSTEM_PROMPT = """\
You are an expert prompt engineer. Given a summary of how a task is performed,
you write a precise, effective system prompt that will turn a general-purpose LLM
into a specialist for that task.

Your output must have two sections:
SYSTEM PROMPT:
<the prompt text>

RATIONALE:
<why you structured it this way>\
"""


def run(scout_output: ScoutOutput, refinement_hint: str = "") -> GeneratedPrompt:
    """
    Write a system prompt from the scout's findings.
    If refinement_hint is provided, incorporate that feedback into the new version.
    """
    # TODO: build user_prompt from scout_output + refinement_hint, call llm.call(), parse response
    raise NotImplementedError
