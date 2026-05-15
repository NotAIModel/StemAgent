from groq import Groq
from openai import OpenAI
import config

_groq_client:   Groq   | None = None
_openai_client: OpenAI | None = None


def _groq() -> Groq:
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=config.GROQ_API_KEY)
    return _groq_client


def _openai() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _openai_client


def call(
    user_prompt: str,
    system_prompt: str = "",
    temperature: float = 0.7,
) -> str:
    """Single LLM call. Provider and model are taken from config.PROVIDER."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    if config.PROVIDER == "openai":
        response = _openai().chat.completions.create(
            model=config.MODEL_OPENAI,
            messages=messages,
            temperature=temperature,
        )
    else:
        response = _groq().chat.completions.create(
            model=config.MODEL_GROQ,
            messages=messages,
            temperature=temperature,
        )

    return response.choices[0].message.content or ""
