from .base import BaseLoader, Document


class TextLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return [Document(content=content, metadata={"source": file_path})]
