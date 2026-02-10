import uuid

import chromadb

from config import CHROMA_PERSIST_DIR, COLLECTION_NAME
from loaders.base import Document


class EmbeddingStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def add_documents(self, documents: list[Document]) -> int:
        """Add documents to the collection. Returns the number of documents added."""
        if not documents:
            return 0

        ids = [str(uuid.uuid4()) for _ in documents]
        contents = [doc.content for doc in documents]
        metadatas = []
        for doc in documents:
            # ChromaDB metadata values must be str, int, float, or bool
            clean = {}
            for k, v in doc.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    clean[k] = v
                else:
                    clean[k] = str(v)
            metadatas.append(clean)

        self.collection.add(ids=ids, documents=contents, metadatas=metadatas)
        return len(ids)

    def query(self, text: str, n_results: int = 5) -> dict:
        """Query the collection and return results."""
        return self.collection.query(query_texts=[text], n_results=n_results)

    def count(self) -> int:
        """Return the number of documents in the collection."""
        return self.collection.count()
