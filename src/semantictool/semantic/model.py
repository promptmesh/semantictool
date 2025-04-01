import asyncio
from semantictool.config.loader import CONFIG

from sentence_transformers import SentenceTransformer

class VectorModel:
    model_name: str
    model: SentenceTransformer

    def __init__(self):
        self.model_name = CONFIG.embedding.model_name

    def load(self):
        self.model = SentenceTransformer(self.model_name) # type: ignore

    async def embed(self, text: str):
        return await asyncio.to_thread(self.model.encode, text)
    
    async def embed_many(self, texts: list[str]):
        return await asyncio.to_thread(self.model.encode, texts, normalize_embeddings=True)
    
VECTORMODEL = VectorModel()