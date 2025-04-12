import numpy as np
from typing import Dict

from semantictool.config.loader import CONFIG

class AsyncSimpleVectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.vectors: Dict[str, np.ndarray] = {}

    async def add(self, tool_id: str, vector: np.ndarray):
        if tool_id in self.vectors:
            raise ValueError(f"Tool {tool_id} already exists")
        self.vectors[tool_id] = vector / np.linalg.norm(vector)

    async def remove(self, tool_id: str):
        self.vectors.pop(tool_id, None)

    async def search(self, query_vec: np.ndarray, k: int = 5) -> list[str]:
        query_norm = query_vec / np.linalg.norm(query_vec)
        items = list(self.vectors.items())
        sims = np.dot(np.stack([v for _, v in items]), query_norm)
        top_k = np.argsort(sims)[::-1][:k]
        return [items[i][0] for i in top_k]
    
    async def get_all(self) -> list[tuple[str, np.ndarray]]:
        return list(self.vectors.items())

STORE = AsyncSimpleVectorStore(dim=CONFIG.embedding.dim)