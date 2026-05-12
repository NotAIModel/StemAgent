"""
Role 1 — Scout
Asks the LLM how code review is typically done and returns a structured summary.
No task-specific knowledge is hard-coded here; the agent figures it out itself.
"""

import llm
from models import ScoutOutput


SYSTEM_PROMPT = """\
You are a research assistant. When asked about a software engineering practice,
you produce a concise, structured summary covering:
- best practices
- common pitfalls reviewers miss
- the dimensions a reviewer should evaluate (e.g. correctness, security, style)

Be specific and practical. Output plain text with clear labeled sections.\
"""


def run() -> ScoutOutput:
    """Ask the LLM how code review is done and parse the response."""
    # TODO: build user_prompt, call llm.call(), parse response into ScoutOutput
    raise NotImplementedError
