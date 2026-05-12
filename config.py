import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Single model used for all roles — swap to test different capabilities
MODEL = "llama-3.3-70b-versatile"

# How many refinement loops the pipeline is allowed before giving up
MAX_REFINEMENT_ROUNDS = 2

# Minimum evaluation score (0–10) before the pipeline accepts the review
QUALITY_THRESHOLD = 7.0
