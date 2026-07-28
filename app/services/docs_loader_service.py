# Load the knowledge base docs from app/docs
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = ROOT_DIR / 'docs'

def load_documents() -> list:
    documents = []
    p = Path(DOCS_DIR)

    for file in p.iterdir():
        if not file.is_file():
            continue
        documents.append(
            {
                'filename': file.name,
                'contents': file.read_text()
            }
        )

    return documents