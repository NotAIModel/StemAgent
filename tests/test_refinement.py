"""
Integration test verifying the refinement loop fires when quality threshold is high.
Forces refinement by temporarily raising config.QUALITY_THRESHOLD to 9.5.
Makes real LLM calls. Requires GROQ_API_KEY to be set (via .env or environment).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import pipeline

SAMPLE_PATH = Path(__file__).parent.parent / "samples" / "sample.py"


def test_refinement_loop_fires():
    original_threshold = config.QUALITY_THRESHOLD
    config.QUALITY_THRESHOLD = 9.5

    try:
        code = SAMPLE_PATH.read_text()
        result = pipeline.run(code)
    finally:
        config.QUALITY_THRESHOLD = original_threshold

    assert result["refinement_rounds"] >= 1, (
        f"Expected at least one refinement round with threshold=9.5, "
        f"but got score={result['evaluation'].score} and refinement_rounds=0"
    )
    assert result["refinement_rounds"] <= config.MAX_REFINEMENT_ROUNDS, (
        f"refinement_rounds={result['refinement_rounds']} exceeded "
        f"MAX_REFINEMENT_ROUNDS={config.MAX_REFINEMENT_ROUNDS}"
    )
