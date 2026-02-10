from loaders.base import Document


def chunk_documents(
    documents: list[Document],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    """Split documents into overlapping chunks, preserving metadata."""
    chunked = []
    for doc in documents:
        text = doc.content
        if len(text) <= chunk_size:
            chunk_doc = Document(
                content=text,
                metadata={**doc.metadata, "chunk_index": 0},
            )
            chunked.append(chunk_doc)
            continue

        start = 0
        chunk_index = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunk_doc = Document(
                content=chunk_text,
                metadata={**doc.metadata, "chunk_index": chunk_index},
            )
            chunked.append(chunk_doc)
            start += chunk_size - chunk_overlap
            chunk_index += 1

    return chunked
