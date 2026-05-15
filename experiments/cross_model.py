"""
Full matrix comparison:
  {Groq, OpenAI} × {baseline, stem agent} × {sample_advanced_clean.py, sample.cpp}
  = 8 combinations × 5 runs = 40 runs total.

Outputs per-combination tables, a summary matrix, and before/after deltas.
Results saved to experiments/results_cross_model.md.
"""

import sys
import statistics
from pathlib import Path
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import baseline as baseline_mod
import pipeline

SAMPLES_DIR  = Path(__file__).parent.parent / "samples"
RESULTS_PATH = Path(__file__).parent / "results_cross_model.md"
N_RUNS = 5

PROVIDERS = ["groq", "openai"]
MODES     = ["baseline", "stem_agent"]
SAMPLES   = ["sample_advanced_clean.py", "sample.cpp"]

PROVIDER_LABEL = {
    "groq":   "Groq (llama-3.3-70b-versatile)",
    "openai": "OpenAI (gpt-4o-mini)",
}
MODE_LABEL = {
    "baseline":   "baseline",
    "stem_agent": "stem agent",
}


@dataclass
class RunResult:
    run: int
    comments: int
    high: int
    medium: int
    low: int
    score: float | None = None            # None for baseline runs
    refinement_rounds: int | None = None  # None for baseline runs


def _to_run_result(run_number: int, review, evaluation=None, refinement_rounds=None) -> RunResult:
    sc = review.severity_counts
    return RunResult(
        run=run_number,
        comments=len(review.comments),
        high=sc["high"],
        medium=sc["medium"],
        low=sc["low"],
        score=evaluation.score if evaluation else None,
        refinement_rounds=refinement_rounds,
    )


def run_baseline(code: str, i: int) -> RunResult:
    review = baseline_mod.run(code)
    return _to_run_result(i, review)


def run_stem_agent(code: str, i: int) -> RunResult:
    result = pipeline.run(code)
    return _to_run_result(
        i, result["review"], result["evaluation"], result["refinement_rounds"]
    )


def comment_stats(runs: list[RunResult]) -> tuple[float, float]:
    vals = [r.comments for r in runs]
    return statistics.mean(vals), (statistics.stdev(vals) if len(vals) > 1 else 0.0)


def format_table(runs: list[RunResult], mode: str) -> str:
    if mode == "stem_agent":
        hdr = f"{'Run':<4} {'Comments':<10} {'High':<6} {'Med':<6} {'Low':<6} {'Score':<7} {'Refines'}"
        rows = [
            f"{r.run:<4} {r.comments:<10} {r.high:<6} {r.medium:<6} {r.low:<6} "
            f"{r.score:<7.1f} {r.refinement_rounds}"
            for r in runs
        ]
    else:
        hdr = f"{'Run':<4} {'Comments':<10} {'High':<6} {'Med':<6} {'Low'}"
        rows = [
            f"{r.run:<4} {r.comments:<10} {r.high:<6} {r.medium:<6} {r.low}"
            for r in runs
        ]
    return "\n".join([hdr, "-" * len(hdr)] + rows)


def main() -> None:
    output: list[str] = []

    def emit(line: str = "") -> None:
        print(line)
        output.append(line)

    # ------------------------------------------------------------------ #
    # Collect all 40 runs                                                 #
    # ------------------------------------------------------------------ #
    # key: (provider, mode, sample_name) -> list[RunResult]
    all_results: dict[tuple, list[RunResult]] = {}
    total = N_RUNS * len(PROVIDERS) * len(MODES) * len(SAMPLES)
    done  = 0

    for provider in PROVIDERS:
        config.PROVIDER = provider
        for sample_name in SAMPLES:
            code = (SAMPLES_DIR / sample_name).read_text()
            for mode in MODES:
                runs: list[RunResult] = []
                for i in range(1, N_RUNS + 1):
                    done += 1
                    print(
                        f"[{done:>2}/{total}] {PROVIDER_LABEL[provider]} | "
                        f"{MODE_LABEL[mode]:<11} | {sample_name} | run {i}",
                        flush=True,
                    )
                    if mode == "baseline":
                        runs.append(run_baseline(code, i))
                    else:
                        runs.append(run_stem_agent(code, i))
                all_results[(provider, mode, sample_name)] = runs

    # ------------------------------------------------------------------ #
    # 1. Per-combination tables                                           #
    # ------------------------------------------------------------------ #
    emit("# Cross-model matrix comparison")
    emit(
        f"Matrix: {{Groq, OpenAI}} × {{baseline, stem agent}} × "
        f"{{sample_advanced_clean.py, sample.cpp}} — {N_RUNS} runs each ({total} total)\n"
    )
    emit("## Per-combination results\n")

    for provider in PROVIDERS:
        for mode in MODES:
            for sample_name in SAMPLES:
                key   = (provider, mode, sample_name)
                runs  = all_results[key]
                label = f"{PROVIDER_LABEL[provider]} / {MODE_LABEL[mode]} / {sample_name}"
                emit(f"### {label}\n")
                emit("```")
                emit(format_table(runs, mode))
                emit("```\n")

    # ------------------------------------------------------------------ #
    # 2. Summary matrix                                                   #
    # ------------------------------------------------------------------ #
    emit("## Summary matrix — mean ± stdev comments\n")

    col_w       = 30
    row_label_w = 44
    emit("```")
    header = f"{'':^{row_label_w}}"
    for s in SAMPLES:
        header += f"  {s:^{col_w}}"
    emit(header)
    emit("-" * (row_label_w + (col_w + 2) * len(SAMPLES)))

    for provider in PROVIDERS:
        for mode in MODES:
            label = f"{PROVIDER_LABEL[provider]} / {MODE_LABEL[mode]}"
            row   = f"{label:<{row_label_w}}"
            for sample_name in SAMPLES:
                mean, stdev = comment_stats(all_results[(provider, mode, sample_name)])
                cell = f"{mean:.1f} ± {stdev:.2f}"
                row += f"  {cell:^{col_w}}"
            emit(row)
    emit("```\n")

    # ------------------------------------------------------------------ #
    # 3. Before/after delta section                                       #
    # ------------------------------------------------------------------ #
    emit("## Baseline → stem agent delta (mean comments)\n")

    for provider in PROVIDERS:
        for sample_name in SAMPLES:
            base_mean, base_std = comment_stats(all_results[(provider, "baseline",   sample_name)])
            stem_mean, stem_std = comment_stats(all_results[(provider, "stem_agent", sample_name)])
            delta = stem_mean - base_mean
            sign  = "+" if delta >= 0 else ""

            emit(f"### {PROVIDER_LABEL[provider]} / {sample_name}\n")
            emit("```")
            emit(f"Baseline:    {base_mean:.1f} ± {base_std:.2f} comments")
            emit(f"Stem agent:  {stem_mean:.1f} ± {stem_std:.2f} comments")
            emit(f"Delta:       {sign}{delta:.1f}")
            emit("```\n")

    RESULTS_PATH.write_text("\n".join(output))
    print(f"\nResults saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
