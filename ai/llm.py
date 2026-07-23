"""
Thin wrapper around a local Ollama model.

Using Ollama keeps this project free to run -- no API key, no per-token
cost -- but it does require Ollama to be installed and running locally
with the model pulled (see README: `ollama pull llama3`).
"""
from langchain_ollama import OllamaLLM

from utils.config import OLLAMA_MODEL
from utils.logger import logger

_llm = OllamaLLM(model=OLLAMA_MODEL)


def ask_ai(prompt: str) -> str:
    try:
        return _llm.invoke(prompt)
    except Exception as e:
        logger.error(f"LLM call failed (is Ollama running? `ollama serve`): {e}")
        raise RuntimeError(
            f"Could not reach the local Ollama model '{OLLAMA_MODEL}'. "
            "Make sure Ollama is installed and running (`ollama serve`) "
            f"and the model is pulled (`ollama pull {OLLAMA_MODEL}`)."
        ) from e
