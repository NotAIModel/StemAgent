"""
Orchestrates the four agents in sequence with an optional refinement loop.
"""

import config
from agents import scout, prompt_engineer, executor, evaluator
from models import ScoutOutput, GeneratedPrompt, Review, Evaluation


def run(code: str) -> dict:
    print("Scouting...")
    scout_output: ScoutOutput = scout.run(code)

    print("Specializing...")
    generated_prompt: GeneratedPrompt = prompt_engineer.run(scout_output)

    review: Review | None = None
    evaluation: Evaluation | None = None
    refinement_rounds = 0

    for _ in range(config.MAX_REFINEMENT_ROUNDS + 1):
        print("Reviewing...")
        review = executor.run(code, generated_prompt)

        print("Evaluating...")
        evaluation = evaluator.run(review)

        if not evaluation.needs_refinement:
            break

        if refinement_rounds >= config.MAX_REFINEMENT_ROUNDS:
            break  # budget exhausted — accept current review

        refinement_rounds += 1
        print(f"Refining (round {refinement_rounds})...")
        generated_prompt = prompt_engineer.run(scout_output)

    return {
        "scout":             scout_output,
        "generated_prompt":  generated_prompt,
        "review":            review,
        "evaluation":        evaluation,
        "refinement_rounds": refinement_rounds,
    }
