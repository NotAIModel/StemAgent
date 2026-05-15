import os
from dotenv import load_dotenv
load_dotenv()

# Provider: "groq" or "openai" — default groq so existing tests are unaffected
PROVIDER = os.environ.get("PROVIDER", "groq")

GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

MODEL_GROQ   = "llama-3.3-70b-versatile"
MODEL_OPENAI = "gpt-4o-mini"

# Legacy alias — used by agents that reference config.MODEL directly
MODEL = MODEL_GROQ

# How many refinement loops the pipeline is allowed before giving up
MAX_REFINEMENT_ROUNDS = 2

# Minimum evaluation score (0–10) before the pipeline accepts the review
QUALITY_THRESHOLD = 7.0
