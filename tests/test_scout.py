"""
Integration test for agents/scout.py — makes a real LLM call.
Requires GROQ_API_KEY to be set (via .env or environment).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scout import run


SAMPLE_PATH = Path(__file__).parent.parent / "samples" / "sample.py"


def test_scout_on_sample():
    code = SAMPLE_PATH.read_text()
    result = run(code)

    assert result.language == "Python"
    assert isinstance(result.focus_areas, list) and len(result.focus_areas) > 0
    assert isinstance(result.risks, list) and len(result.risks) > 0
    assert isinstance(result.reviewer_persona, str) and len(result.reviewer_persona) > 0
