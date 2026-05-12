import sys
import pipeline


def load_code(path: str) -> str:
    with open(path) as f:
        return f.read()


def print_result(result) -> None:
    sep = "-" * 60

    print(sep)
    print("BASELINE REVIEW (generic, no specialization)")
    print(sep)
    print(result.baseline_review.content)

    print(sep)
    print("GENERATED SYSTEM PROMPT")
    print(sep)
    print(result.generated_prompt.system_prompt)
    print(f"\nRationale: {result.generated_prompt.rationale}")

    print(sep)
    print("SPECIALIZED REVIEW")
    print(sep)
    print(result.specialized_review.content)

    print(sep)
    print("EVALUATION")
    print(sep)
    ev = result.evaluation
    print(f"Score: {ev.score}/10  |  Rounds: {result.rounds}")
    print("Strengths:", ", ".join(ev.strengths) or "—")
    print("Weaknesses:", ", ".join(ev.weaknesses) or "—")


if __name__ == "__main__":
    code_path = sys.argv[1] if len(sys.argv) > 1 else "samples/sample.py"
    code = load_code(code_path)
    result = pipeline.run(code)
    print_result(result)
