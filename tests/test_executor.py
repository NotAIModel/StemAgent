"""
Integration test for agents/executor.py — chains scout → prompt engineer → executor.
Makes real LLM calls. Requires GROQ_API_KEY to be set (via .env or environment).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scout import run as scout_run
from agents.prompt_engineer import run as pe_run
from agents.executor import run as exec_run

SAMPLE_PATH = Path(__file__).parent.parent / "samples" / "sample.py"


def test_executor_on_python_sample():
    code = SAMPLE_PATH.read_text()
    scout_output = scout_run(code)
    generated_prompt = pe_run(scout_output)
    result = exec_run(code, generated_prompt)

    assert isinstance(result.comments, list) and len(result.comments) > 0
    assert isinstance(result.summary, str) and len(result.summary) > 0
    assert set(result.severity_counts.keys()) == {"high", "medium", "low"}
    assert all(isinstance(v, int) for v in result.severity_counts.values())
