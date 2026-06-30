import pytest

from app.rag.chunker import split_text


def test_text_shorter_than_chunk_size_returns_a_single_chunk():

    assert split_text("hello world", chunk_size=500, chunk_overlap=50) == ["hello world"]


def test_text_longer_than_chunk_size_is_split_with_overlap():

    text = "0123456789" * 3

    chunks = split_text(text, chunk_size=10, chunk_overlap=2)

    assert chunks == ["0123456789", "8901234567", "6789012345", "456789"]
    assert "".join(chunks) != text


def test_chunk_overlap_must_be_smaller_than_chunk_size():

    with pytest.raises(ValueError):
        split_text("some text", chunk_size=10, chunk_overlap=10)
