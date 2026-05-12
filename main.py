import sys
import pipeline


def print_result(result: dict) -> None:
    sep = "-" * 60
    scout    = result["scout"]
    prompt   = result["generated_prompt"]
    review   = result["review"]
    ev       = result["evaluation"]
    rounds   = result["refinement_rounds"]

    print(f"\n{'=' * 60}")
    print("  SCOUT")
    print(f"{'=' * 60}")
    print(f"language        : {scout.language}")
    print(f"reviewer_persona: {scout.reviewer_persona}")
    print(f"focus_areas     : {', '.join(scout.focus_areas)}")
    print(f"risks ({len(scout.risks)}):")
    for r in scout.risks:
        print(f"  • {r}")

    print(f"\n{'=' * 60}")
    print("  GENERATED SYSTEM PROMPT")
    print(f"{'=' * 60}")
    print(prompt.system_prompt)
    print(f"\nselected_tools: {prompt.selected_tools}")

    print(f"\n{'=' * 60}")
    print("  REVIEW")
    print(f"{'=' * 60}")
    sc = review.severity_counts
    print(f"severity: {sc['high']} high  {sc['medium']} medium  {sc['low']} low")
    print(f"comments ({len(review.comments)}):")
    for c in review.comments:
        print(f"  • {c}")
    print(f"\nsummary:\n{review.summary}")

    print(f"\n{'=' * 60}")
    print("  EVALUATION")
    print(f"{'=' * 60}")
    print(f"score           : {ev.score}/10")
    print(f"needs_refinement: {ev.needs_refinement}  (refinement rounds used: {rounds})")
    print(f"reasoning:\n{ev.reasoning}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "samples/sample.py"
    with open(path) as f:
        code = f.read()
    result = pipeline.run(code)
    print_result(result)
