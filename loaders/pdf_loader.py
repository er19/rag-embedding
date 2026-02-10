import fitz

from .base import BaseLoader, Document


class PDFLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        documents = []
        with fitz.open(file_path) as pdf:
            for page_num, page in enumerate(pdf, start=1):
                text = page.get_text()
                if text.strip():
                    documents.append(
                        Document(
                            content=text,
                            metadata={"source": file_path, "page": page_num},
                        )
                    )
        return documents
