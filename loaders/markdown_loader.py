import markdown
from bs4 import BeautifulSoup

from .base import BaseLoader, Document


class MarkdownLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        with open(file_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        html = markdown.markdown(md_text)
        plain_text = BeautifulSoup(html, "html.parser").get_text()
        return [Document(content=plain_text, metadata={"source": file_path})]
