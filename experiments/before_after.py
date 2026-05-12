"""
Before/after comparison: baseline (no specialization) vs stem agent (full pipeline).
Both run on the same file so every difference is attributable to specialization alone.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import baseline
from agents.scout import run as scout_run
from agents.prompt_engineer import run as pe_run
from agents.executor import run as exec_run
from models import Review

DEFAULT_SAMPLE = Path(__file__).parent.parent / "samples" / "sample.py"


def run_stem_agent(code: str) -> Review:
    scout_output     = scout_run(code)
    generated_prompt = pe_run(scout_output)
    return exec_run(code, generated_prompt)


def print_review(label: str, review: Review) -> None:
    sep = "-" * 55
    print(f"\n{sep}")
    print(f"  {label}")
    print(sep)
    sc = review.severity_counts
    print(f"comments      : {len(review.comments)}")
    print(f"severity      : {sc['high']} high  {sc['medium']} medium  {sc['low']} low")
    print(f"summary:\n  {review.summary}")


def main() -> None:
    sample = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SAMPLE
    print(f"File: {sample.name}\n")
    code = sample.read_text()

    print("Running baseline ...")
    base = baseline.run(code)

    print("Running stem agent (scout → prompt engineer → executor) ...")
    stem = run_stem_agent(code)

    print_review("BASELINE  (no specialization)", base)
    print_review("STEM AGENT  (self-specialized)", stem)

    sep = "=" * 55
    print(f"\n{sep}")
    print("  DELTA")
    print(sep)
    comment_delta = len(stem.comments) - len(base.comments)
    sign = "+" if comment_delta >= 0 else ""
    print(f"comments      : {sign}{comment_delta}  ({len(base.comments)} → {len(stem.comments)})")

    for key in ("high", "medium", "low"):
        d = stem.severity_counts[key] - base.severity_counts[key]
        sign = "+" if d >= 0 else ""
        print(f"{key:<14}: {sign}{d}  ({base.severity_counts[key]} → {stem.severity_counts[key]})")


if __name__ == "__main__":
    main()
