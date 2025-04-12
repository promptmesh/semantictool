import asyncio
import numpy as np
from sklearn.cluster import DBSCAN

from semantictool.semantic.store import STORE

class Clusters:
    result = None

    def __init__(self):
        self.dbscan = DBSCAN(eps=0.5, min_samples=2)

    async def fit(self, vectors: list[tuple[str, np.ndarray]]):
        self.result = await asyncio.to_thread(self._fit, await STORE.get_all())

    def _fit(self, vectors: list[tuple[str, np.ndarray]]) -> dict[int, list[str]]:
        tool_ids, raw_data = zip(*vectors)
        data = np.stack(raw_data)

        self.dbscan.fit(data)
        labels = self.dbscan.labels_

        clustered_tools: dict[int, list[str]] = {}
        for label, tool_id in zip(labels, tool_ids):
            if label == -1:
                continue  # Ignore "outliers" - tools that do not have duplicates
            clustered_tools.setdefault(label, []).append(tool_id)

        return clustered_tools

    async def get(self):
        return self.result.copy() if self.result else None
    
CLUSTER = Clusters()