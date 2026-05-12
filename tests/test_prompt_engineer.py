"""
Integration test for agents/prompt_engineer.py — makes real LLM calls (scout + prompt engineer).
Requires GROQ_API_KEY to be set (via .env or environment).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scout import run as scout_run
from agents.prompt_engineer import run as pe_run, AVAILABLE_TOOLS

SAMPLE_PATH = Path(__file__).parent.parent / "samples" / "sample.py"


def test_prompt_engineer_on_python_sample():
    code = SAMPLE_PATH.read_text()
    scout_output = scout_run(code)
    result = pe_run(scout_output)

    assert isinstance(result.system_prompt, str) and len(result.system_prompt) > 0
    assert isinstance(result.selected_tools, list) and len(result.selected_tools) > 0
    assert all(t in AVAILABLE_TOOLS for t in result.selected_tools)
    assert "security" in result.system_prompt.lower()
