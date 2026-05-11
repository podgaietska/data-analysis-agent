"""Returns a configured ChatOllama instance."""

import os
from langchain_ollama import ChatOllama

DEFAULT_MODEL = "qwen2.5:7b"


def load_llm() -> ChatOllama:
    model = os.environ.get("LLM_MODEL", DEFAULT_MODEL)
    return ChatOllama(model=model, temperature=0)
