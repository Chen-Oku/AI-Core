import uuid

from app.rag.chroma_client import create_chroma_client, get_or_create_collection
from app.rag.chroma_vector_store import ChromaVectorStore


def _make_store():

    client = create_chroma_client("localhost", 8000)
    collection_name = f"test_{uuid.uuid4().hex}"
    collection = get_or_create_collection(client, collection_name)

    return client, collection_name, ChromaVectorStore(collection)


def test_query_returns_the_closest_match_first():

    client, collection_name, store = _make_store()

    try:
        store.add("doc1", "the sky is blue", [1.0, 0.0], {"source": "a"})
        store.add("doc2", "cats are mammals", [0.0, 1.0], {"source": "b"})

        results = store.query([1.0, 0.0], top_k=2)

        assert results[0]["text"] == "the sky is blue"
        assert results[0]["metadata"] == {"source": "a"}
        assert len(results) == 2
    finally:
        client.delete_collection(collection_name)


def test_add_without_metadata_is_allowed():

    client, collection_name, store = _make_store()

    try:
        store.add("doc1", "no metadata here", [1.0, 0.0])

        results = store.query([1.0, 0.0], top_k=1)

        assert results[0]["text"] == "no metadata here"
        assert results[0]["metadata"] is None
    finally:
        client.delete_collection(collection_name)
