"""
Full pipeline integration test: scout → prompt engineer → executor.

Runs on both sample files and verifies:
- each stage produces valid structured output
- the two runs produce different reviewer_persona values (specialization proof)

Use -s to see the printed intermediate outputs:
    venv/bin/pytest tests/test_pipeline_integration.py -v -s
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scout import run as scout_run
from agents.prompt_engineer import run as pe_run, AVAILABLE_TOOLS
from agents.executor import run as exec_run
from models import ScoutOutput, GeneratedPrompt, Review

ROOT = Path(__file__).parent.parent
SAMPLES = {
    "Python": ROOT / "samples" / "sample.py",
    "C++":    ROOT / "samples" / "sample.cpp",
}


def run_chain(label: str, path: Path) -> tuple[ScoutOutput, GeneratedPrompt, Review]:
    code = path.read_text()

    scout_output    = scout_run(code)
    generated_prompt = pe_run(scout_output)
    review          = exec_run(code, generated_prompt)

    sep = "-" * 60
    print(f"\n{'=' * 60}")
    print(f"  {label} — {path.name}")
    print(f"{'=' * 60}")

    print(f"\n{sep}")
    print("SCOUT OUTPUT")
    print(sep)
    print(f"language        : {scout_output.language}")
    print(f"reviewer_persona: {scout_output.reviewer_persona}")
    print(f"focus_areas     : {', '.join(scout_output.focus_areas)}")
    print(f"risks ({len(scout_output.risks)}):")
    for r in scout_output.risks:
        print(f"  • {r}")

    print(f"\n{sep}")
    print("GENERATED SYSTEM PROMPT")
    print(sep)
    print(generated_prompt.system_prompt)
    print(f"\nselected_tools: {generated_prompt.selected_tools}")

    print(f"\n{sep}")
    print("REVIEW")
    print(sep)
    print(f"severity_counts : {review.severity_counts}")
    print(f"comments ({len(review.comments)}):")
    for c in review.comments:
        print(f"  • {c}")
    print(f"\nsummary:\n{review.summary}")

    return scout_output, generated_prompt, review


def assert_valid(label: str, scout: ScoutOutput, prompt: GeneratedPrompt, review: Review) -> None:
    assert len(review.comments) > 0,             f"{label}: review.comments is empty"
    assert len(review.summary) > 0,              f"{label}: review.summary is empty"
    assert set(review.severity_counts.keys()) == {"high", "medium", "low"}, \
        f"{label}: severity_counts missing keys — got {review.severity_counts}"
    assert all(isinstance(v, int) for v in review.severity_counts.values()), \
        f"{label}: severity_counts values must be ints"
    assert len(prompt.selected_tools) > 0,       f"{label}: selected_tools is empty"
    assert all(t in AVAILABLE_TOOLS for t in prompt.selected_tools), \
        f"{label}: unknown tool(s) in selected_tools: {prompt.selected_tools}"


def test_full_pipeline_both_samples():
    results: dict[str, tuple[ScoutOutput, GeneratedPrompt, Review]] = {}

    for label, path in SAMPLES.items():
        results[label] = run_chain(label, path)

    for label, (scout, prompt, review) in results.items():
        assert_valid(label, scout, prompt, review)

    py_persona  = results["Python"][0].reviewer_persona
    cpp_persona = results["C++"][0].reviewer_persona
    print(f"\n{'=' * 60}")
    print("SPECIALIZATION PROOF")
    print(f"{'=' * 60}")
    print(f"Python persona : {py_persona}")
    print(f"C++    persona : {cpp_persona}")
    assert py_persona != cpp_persona, (
        "Specialization failed: both samples produced the same reviewer_persona.\n"
        f"  Python : {py_persona}\n"
        f"  C++    : {cpp_persona}"
    )
