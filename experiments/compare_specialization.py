"""
Demonstrates environment-driven specialization.

Runs scout.run() on two different code samples and prints a side-by-side
comparison of the specialization specs. The same agent, different inputs,
different outputs — no hardcoded logic.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scout import run
from models import ScoutOutput

SAMPLES = {
    "Python": Path(__file__).parent.parent / "samples" / "sample.py",
    "C++":    Path(__file__).parent.parent / "samples" / "sample.cpp",
}


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def show(label: str, spec: ScoutOutput) -> None:
    print(f"\n--- {label} ---")
    print(f"language        : {spec.language}")
    print(f"reviewer_persona: {spec.reviewer_persona}")
    print(f"focus_areas     : {', '.join(spec.focus_areas)}")
    print(f"risks ({len(spec.risks)}):")
    for risk in spec.risks:
        print(f"  • {risk}")


def main() -> None:
    specs: dict[str, ScoutOutput] = {}

    for label, path in SAMPLES.items():
        print(f"\nRunning scout on {path.name} ...")
        code = path.read_text()
        specs[label] = run(code)

    section("SPECIALIZATION COMPARISON")
    for label, spec in specs.items():
        show(label, spec)

    section("KEY DIFFERENCES")
    all_labels = list(specs.keys())
    a, b = all_labels[0], all_labels[1]

    a_areas = set(specs[a].focus_areas)
    b_areas = set(specs[b].focus_areas)
    only_a = a_areas - b_areas
    only_b = b_areas - a_areas
    shared = a_areas & b_areas

    print(f"\nfocus_areas only in {a} : {', '.join(only_a) or '(none)'}")
    print(f"focus_areas only in {b}  : {', '.join(only_b) or '(none)'}")
    print(f"shared focus_areas       : {', '.join(shared) or '(none)'}")


if __name__ == "__main__":
    main()
