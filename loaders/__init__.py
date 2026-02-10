from .base import Document, BaseLoader
from .text_loader import TextLoader
from .pdf_loader import PDFLoader
from .markdown_loader import MarkdownLoader
from .image_loader import ImageLoader
from .docx_loader import DocxLoader
from .excel_loader import ExcelLoader

LOADER_MAP = {
    ".txt": TextLoader,
    ".pdf": PDFLoader,
    ".md": MarkdownLoader,
    ".png": ImageLoader,
    ".jpg": ImageLoader,
    ".jpeg": ImageLoader,
    ".docx": DocxLoader,
    ".xlsx": ExcelLoader,
}

__all__ = [
    "Document",
    "BaseLoader",
    "TextLoader",
    "PDFLoader",
    "MarkdownLoader",
    "ImageLoader",
    "DocxLoader",
    "ExcelLoader",
    "LOADER_MAP",
]
