from dataclasses import dataclass, field


@dataclass
class ScoutOutput:
    """What the scout inferred by analyzing the code sample."""
    language: str = ""
    focus_areas: list[str] = field(default_factory=list)   # e.g. ["security", "error handling"]
    risks: list[str] = field(default_factory=list)          # concrete risks spotted in this code
    reviewer_persona: str = ""                              # e.g. "security-focused senior engineer"
    raw: str = ""                                           # raw LLM response, kept for debugging


@dataclass
class GeneratedPrompt:
    """System prompt produced by the prompt engineer."""
    system_prompt: str = ""
    selected_tools: list[str] = field(default_factory=list)
    raw: str = ""


@dataclass
class Review:
    """Code review produced by the executor."""
    content: str = ""
    system_prompt_used: str = ""  # which system prompt drove this review


@dataclass
class Evaluation:
    """Evaluator's assessment of a review."""
    score: float = 0.0          # 0–10
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    refinement_needed: bool = False
    refinement_hint: str = ""   # passed back to prompt engineer on re-run
    raw: str = ""


@dataclass
class PipelineResult:
    """Full output of one stem-agent run."""
    scout_output: ScoutOutput | None = None
    generated_prompt: GeneratedPrompt | None = None
    baseline_review: Review | None = None
    specialized_review: Review | None = None
    evaluation: Evaluation | None = None
    rounds: int = 0             # how many refinement loops ran
