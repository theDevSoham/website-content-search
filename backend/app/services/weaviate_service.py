# app/services/weaviate_service.py
from __future__ import annotations
import uuid
from typing import Iterable, List, Optional, Sequence, Tuple

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import (
    Property, DataType, Configure, VectorDistances
)
import weaviate.classes.query as wq

from app.core.config import get_settings

env = get_settings()


class WeaviateService:
    """
    - Uses BYO vectors (we compute embeddings with HF, not in Weaviate)
    - Single default vector space (no named vectors)
    """
    def __init__(self) -> None:
        # Keep this client open for the app lifetime
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=env.WEAVIATE_URL,
            auth_credentials=Auth.api_key(env.WEAVIATE_API_KEY),
        )
        self.collection_name = env.WEAVIATE_COLLECTION
        self.collection = self._ensure_collection()

    def _ensure_collection(self):
        existing = {c for c in self.client.collections.list_all().keys()}
        print(existing)
        if self.collection_name in existing:
            return self.client.collections.get(self.collection_name)

        # NEW API: use vector_config (not vectorizer_config)
        # BYO vectors -> Configure.Vectors.self_provided(...)
        return self.client.collections.create(
            name=self.collection_name,
            properties=[
                Property(name="url", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT),
                Property(name="chunk_index", data_type=DataType.INT),
                Property(name="tokens", data_type=DataType.INT),
            ],
            vector_config=Configure.Vectors.self_provided(
                # HNSW w/ cosine is typical for text embeddings
                vector_index_config=Configure.VectorIndex.hnsw(
                    distance_metric=VectorDistances.COSINE
                )
            ),
        )

    # ---------- Ingestion ----------

    @staticmethod
    def _chunk_uuid(url: str, chunk_index: int) -> uuid.UUID:
        # Stable UUID so re-ingestion overwrites instead of duplicating
        return uuid.uuid5(uuid.NAMESPACE_URL, f"{url}#{chunk_index}")

    def upsert_chunks(
        self,
        url: str,
        chunks: Sequence[str],
        embeddings: Sequence[Sequence[float]],
        token_counts: Optional[Sequence[int]] = None,
    ) -> None:
        assert len(chunks) == len(embeddings), "chunks and embeddings must align"
        if token_counts is not None:
            assert len(token_counts) == len(chunks), "token_counts length mismatch"

        with self.collection.batch.dynamic() as batch:
            for i, (content, vector) in enumerate(zip(chunks, embeddings)):
                props = {
                    "url": url,
                    "content": content,
                    "chunk_index": i,
                }
                if token_counts is not None:
                    props["tokens"] = int(token_counts[i])

                batch.add_object(
                    properties=props,
                    uuid=self._chunk_uuid(url, i),
                    vector=vector,  # BYO vector for default vector space
                )

    # ---------- Search ----------

    def search_near_vector(
        self,
        query_vector: Sequence[float],
        limit: int = 10,
        target_url: Optional[str] = None,
    ):
        """
        Vector similarity search. Optionally filter by URL.
        """
        where_filter = None
        if target_url:
            # Simple equality filter on url
            where_filter = wq.Filter.by_property("url").equal(target_url)

        results = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            return_metadata=wq.MetadataQuery(distance=True),
            filters=where_filter,
        )

        # Normalize into a light dict structure
        out = []
        for obj in results.objects:
            out.append({
                "uuid": str(obj.uuid),
                "url": obj.properties.get("url"),
                "chunk_index": obj.properties.get("chunk_index"),
                "tokens": obj.properties.get("tokens"),
                "content": obj.properties.get("content"),
                "distance": getattr(obj.metadata, "distance", None),
            })
        return out

    # ---------- Teardown ----------

    def close(self):
        try:
            self.client.close()
        except Exception:
            pass
