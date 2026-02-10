from PIL import Image
import pytesseract

from .base import BaseLoader, Document


class ImageLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return [Document(content=text, metadata={"source": file_path})]
