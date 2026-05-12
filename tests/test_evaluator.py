"""
Integration test for agents/evaluator.py — chains the full pipeline.
Makes real LLM calls. Requires GROQ_API_KEY to be set (via .env or environment).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scout import run as scout_run
from agents.prompt_engineer import run as pe_run
from agents.executor import run as exec_run
from agents.evaluator import run as eval_run

SAMPLE_PATH = Path(__file__).parent.parent / "samples" / "sample.py"


def test_evaluator_on_python_sample():
    code = SAMPLE_PATH.read_text()
    scout_output     = scout_run(code)
    generated_prompt = pe_run(scout_output)
    review           = exec_run(code, generated_prompt)
    result           = eval_run(review)

    assert isinstance(result.score, float),          "score must be a float"
    assert 0.0 <= result.score <= 10.0,              f"score out of range: {result.score}"
    assert isinstance(result.needs_refinement, bool), "needs_refinement must be a bool"
    assert isinstance(result.reasoning, str) and len(result.reasoning) > 0, "reasoning is empty"
