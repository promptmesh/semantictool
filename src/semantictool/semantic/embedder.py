import asyncio
import numpy as np
import redis.asyncio as redis
from hashlib import sha1

from semantictool.semantic.model import VECTORMODEL
from semantictool.config.loader import CONFIG

REDIS = redis.from_url(CONFIG.redis.url, decode_responses=False)
CONCURRENCY_LIMIT = 16

def serialize_vector(vec: np.ndarray) -> bytes:
    return vec.astype(np.float32).tobytes()

def deserialize_vector(data: bytes) -> np.ndarray:
    return np.frombuffer(data, dtype=np.float32)

def make_redis_key(description: str) -> str:
    return f"embedding:{sha1(description.encode()).hexdigest()}"


async def get_cached_vector(description: str) -> np.ndarray | None:
    key = make_redis_key(description)
    cached = await REDIS.get(key)
    return deserialize_vector(cached) if cached else None


async def cache_vector(description: str, vector: np.ndarray):
    key = make_redis_key(description)
    await REDIS.set(key, serialize_vector(vector))


async def embed_or_get_vector(description: str) -> np.ndarray:
    cached = await get_cached_vector(description)
    if cached is not None:
        return cached

    vector = await VECTORMODEL.embed(description)
    await cache_vector(description, vector)
    return vector


async def process_tool(tool, semaphore: asyncio.Semaphore) -> tuple[str, np.ndarray] | None:
    async with semaphore:
        try:
            vector = await embed_or_get_vector(tool.description)
            return tool.name, vector
        except Exception as e:
            print(f"[embed] Failed for {tool.name}: {e}")
            return None
