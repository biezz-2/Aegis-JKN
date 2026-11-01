"""
Aegis-JKN Embedding Service.
Configured via .env variables to compute semantic vector embeddings for
clinical narratives, diagnosis codes, and patient feedback.
Includes automatic fallback between primary and secondary embedding models.
"""

import os
import json
import logging
from typing import List, Optional
import urllib.request
import urllib.error
from dotenv import load_dotenv, find_dotenv

# Search upward from current file to find the nearest .env
load_dotenv(find_dotenv(usecwd=True))

logger = logging.getLogger(__name__)

EMBEDDING_ENDPOINT = os.getenv("EMBEDDING_ENDPOINT", "https://9router.biezz.my.id/v1/embeddings")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")
PRIMARY_MODEL = os.getenv("EMBEDDING_MODEL_NAME", "openrouter/openai/text-embedding-3-large")
FALLBACK_MODEL = os.getenv("EMBEDDING_FALLBACK_MODEL", "openrouter/nvidia/llama-nemotron-embed-vl-1b-v2:free")


def get_headers() -> dict:
    key = os.getenv("EMBEDDING_API_KEY", EMBEDDING_API_KEY)
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "Aegis-JKN-Embedding-Service/1.0"
    }


def call_embedding_api(text: str, model_name: str) -> List[float]:
    """Calls the embedding endpoint for a single text input."""
    payload = {
        "model": model_name,
        "input": text
    }

    req = urllib.request.Request(
        EMBEDDING_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers()
    )

    with urllib.request.urlopen(req, timeout=45) as response:
        raw = response.read().decode("utf-8")
        clean = raw.split("data: [DONE]")[0].strip()
        data = json.loads(clean)
        return data["data"][0]["embedding"]


def get_embedding(text: str) -> List[float]:
    """
    Computes an embedding vector for the given text.
    First tries the primary high-precision model, falling back to the secondary model if an error occurs.
    """
    primary = os.getenv("EMBEDDING_MODEL_NAME", PRIMARY_MODEL)
    fallback = os.getenv("EMBEDDING_FALLBACK_MODEL", FALLBACK_MODEL)

    try:
        return call_embedding_api(text, primary)
    except Exception as e:
        logger.warning(f"Primary embedding model '{primary}' failed: {e}. Falling back to '{fallback}'...")
        try:
            return call_embedding_api(text, fallback)
        except Exception as e2:
            logger.error(f"Fallback embedding model '{fallback}' also failed: {e2}")
            raise RuntimeError(f"Gagal menghasilkan embedding: {e2}")


def batch_get_embeddings(texts: List[str]) -> List[List[float]]:
    """Computes embeddings for a batch of texts."""
    return [get_embedding(t) for t in texts]
