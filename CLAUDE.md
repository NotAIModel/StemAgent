# Stem Agent — Project Context

## Architecture
Single LLM (Groq, llama-3.3-70b-versatile), four sequential roles:
1. Scout — analyzes code sample, outputs JSON specialization spec
2. Prompt Engineer — takes spec, writes system prompt + selects tools
3. Executor — runs code review using generated system prompt
4. Evaluator — scores review 0-10, triggers refinement if below threshold

## Rules
- All inter-agent communication in JSON
- No LangChain or agent frameworks — raw API calls only
- Every agent has one job, one file
- Pydantic for output validation

## Current task
Implementing scout.py — analyze a code sample and output a SpecializationSpec