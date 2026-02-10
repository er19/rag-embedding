# RAG Document Embeddings Pipeline

A document embeddings pipeline for Retrieval-Augmented Generation (RAG). Ingests documents in multiple formats, chunks them, generates embeddings using ChromaDB's default model (all-MiniLM-L6-v2), and stores them for semantic search retrieval.

## Supported Formats

| Format | Extensions | Library |
|--------|-----------|---------|
| Plain text | `.txt` | Built-in |
| PDF | `.pdf` | PyMuPDF |
| Markdown | `.md` | markdown + BeautifulSoup |
| Images (OCR) | `.png`, `.jpg`, `.jpeg` | pytesseract + Pillow |
| Word | `.docx` | python-docx |
| Excel | `.xlsx` | openpyxl |

## Setup

```bash
pip install -r requirements.txt
```

For image OCR support, [Tesseract](https://github.com/tesseract-ocr/tesseract) must be installed separately and available on your PATH.

## Usage

### Ingest documents

Recursively scans a directory for supported files, chunks them, and stores embeddings in ChromaDB:

```bash
python main.py ingest ./path/to/documents
```

### Query

Search ingested documents by semantic similarity:

```bash
python main.py query "your search query"
python main.py query "your search query" --n 10
```

The `--n` flag controls the number of results returned (default: 5).

## Project Structure

```
rag-embeddings/
├── requirements.txt          # Dependencies
├── config.py                 # Configuration (chunk size, ChromaDB settings)
├── main.py                   # CLI entry point (ingest + query)
├── loaders/
│   ├── __init__.py           # Loader registry (extension -> loader mapping)
│   ├── base.py               # Document dataclass and BaseLoader ABC
│   ├── text_loader.py        # Plain text
│   ├── pdf_loader.py         # PDF (per-page extraction)
│   ├── markdown_loader.py    # Markdown (strips markup)
│   ├── image_loader.py       # OCR via pytesseract
│   ├── docx_loader.py        # Word documents
│   └── excel_loader.py       # Excel spreadsheets (per-sheet)
├── chunker.py                # Text chunking with configurable overlap
├── embeddings.py             # ChromaDB collection management
└── query.py                  # Query interface with formatted output
```

## Configuration

Edit `config.py` to adjust settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `CHUNK_SIZE` | 500 | Chunk size in characters |
| `CHUNK_OVERLAP` | 50 | Overlap between chunks in characters |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB storage directory |
| `COLLECTION_NAME` | `documents` | ChromaDB collection name |

## Pipeline

```
Files in directory
  → Detect format by extension
  → Route to appropriate loader
  → loader.load() returns list[Document]
  → Chunker splits into overlapping chunks
  → ChromaDB embeds (all-MiniLM-L6-v2) and stores chunks with metadata
```

Each `Document` carries metadata (source file path, page number, sheet name, chunk index) that is preserved through the pipeline and returned with query results.
"# rag-embedding" 
