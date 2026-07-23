"""
Persistent local vector memory using Chroma.

NOTE: the original version of this file created a chromadb.Client()
(in-memory, non-persistent) and a collection, but never defined
add_memory/search_memory even though ai/memory_manager.py imports them
-- that import would fail immediately. Both functions are implemented
here, and storage is switched to a PersistentClient so memories survive
across runs.
"""
import uuid

import chromadb

from ai.embeddings import create_embeddings

_client = chromadb.PersistentClient(path="data/chroma")
_collection = _client.get_or_create_collection(name="memory")


def add_memory(text, metadata=None):
    embedding = create_embeddings(text)
    _collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata or {}],
    )


def search_memory(query, n_results=5):
    embedding = create_embeddings(query)
    return _collection.query(query_embeddings=[embedding], n_results=n_results)
