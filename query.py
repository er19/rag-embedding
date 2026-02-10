from embeddings import EmbeddingStore


def run_query(query_text: str, n_results: int = 5) -> None:
    """Query the embedding store and print formatted results."""
    store = EmbeddingStore()
    total = store.count()
    if total == 0:
        print("No documents in the store. Run 'ingest' first.")
        return

    results = store.query(query_text, n_results=n_results)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not documents:
        print("No results found.")
        return

    print(f"\nQuery: {query_text}")
    print(f"Results ({len(documents)} of {total} chunks):\n")

    for i, (text, metadata, distance) in enumerate(
        zip(documents, metadatas, distances), start=1
    ):
        similarity = 1 - distance  # ChromaDB uses L2 distance by default
        source = metadata.get("source", "unknown")
        chunk_index = metadata.get("chunk_index", "?")

        print(f"--- Result {i} (similarity: {similarity:.4f}) ---")
        print(f"Source: {source} | Chunk: {chunk_index}")
        # Show extra metadata fields
        extra = {k: v for k, v in metadata.items() if k not in ("source", "chunk_index")}
        if extra:
            print(f"Metadata: {extra}")
        print(text[:300])
        if len(text) > 300:
            print("...")
        print()
