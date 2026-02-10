from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Document:
    content: str
    metadata: dict = field(default_factory=dict)


class BaseLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> list[Document]:
        """Load a file and return a list of Document objects."""
        ...
