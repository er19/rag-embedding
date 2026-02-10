import argparse
import os
import sys

from config import CHUNK_SIZE, CHUNK_OVERLAP
from loaders import LOADER_MAP
from chunker import chunk_documents
from embeddings import EmbeddingStore
from query import run_query


def ingest(directory: str) -> None:
    """Discover files in a directory, load, chunk, and store them."""
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    all_documents = []
    supported_extensions = set(LOADER_MAP.keys())

    for root, _dirs, files in os.walk(directory):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in supported_extensions:
                continue

            file_path = os.path.join(root, filename)
            loader_cls = LOADER_MAP[ext]
            loader = loader_cls()

            try:
                docs = loader.load(file_path)
                all_documents.extend(docs)
                print(f"Loaded: {file_path} ({len(docs)} document(s))")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    if not all_documents:
        print("No supported files found.")
        return

    chunks = chunk_documents(all_documents, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"\nChunked {len(all_documents)} document(s) into {len(chunks)} chunk(s).")

    store = EmbeddingStore()
    added = store.add_documents(chunks)
    print(f"Stored {added} chunk(s) in ChromaDB. Total: {store.count()}")


def main():
    parser = argparse.ArgumentParser(description="RAG Document Embeddings Pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents from a directory")
    ingest_parser.add_argument("directory", help="Path to directory containing documents")

    # query command
    query_parser = subparsers.add_parser("query", help="Query the document store")
    query_parser.add_argument("text", help="Query text")
    query_parser.add_argument("--n", type=int, default=5, help="Number of results (default: 5)")

    args = parser.parse_args()

    if args.command == "ingest":
        ingest(args.directory)
    elif args.command == "query":
        run_query(args.text, n_results=args.n)


if __name__ == "__main__":
    main()
