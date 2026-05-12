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
    comments: list[str] = field(default_factory=list)
    severity_counts: dict = field(default_factory=lambda: {"high": 0, "medium": 0, "low": 0})
    summary: str = ""
    raw: str = ""


@dataclass
class Evaluation:
    """Evaluator's assessment of a review."""
    score: float = 0.0
    reasoning: str = ""
    needs_refinement: bool = False  # True when score < config.QUALITY_THRESHOLD
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
