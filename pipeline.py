"""
Orchestrates the four agents in sequence.
Handles the refinement loop: if the evaluator scores below the threshold,
it sends the hint back to the prompt engineer and re-runs executor + evaluator.
"""

import config
import baseline
from agents import scout, prompt_engineer, executor, evaluator
from models import PipelineResult


def run(code: str) -> PipelineResult:
    result = PipelineResult()

    # Step 0 — baseline (generic, no specialization)
    result.baseline_review = baseline.run(code)

    # Step 1 — scout
    result.scout_output = scout.run()

    # Step 2 — prompt engineer (initial pass)
    result.generated_prompt = prompt_engineer.run(result.scout_output)

    # Steps 3 + 4 — execute then evaluate, with optional refinement loop
    refinement_hint = ""
    for round_num in range(1, config.MAX_REFINEMENT_ROUNDS + 2):
        result.rounds = round_num

        if round_num > 1:
            # Re-run prompt engineer with feedback before re-executing
            result.generated_prompt = prompt_engineer.run(
                result.scout_output, refinement_hint=refinement_hint
            )

        result.specialized_review = executor.run(code, result.generated_prompt)
        result.evaluation = evaluator.run(result.specialized_review)

        if not result.evaluation.refinement_needed:
            break
        if round_num >= config.MAX_REFINEMENT_ROUNDS + 1:
            break  # exhausted budget

        refinement_hint = result.evaluation.refinement_hint

    return result
