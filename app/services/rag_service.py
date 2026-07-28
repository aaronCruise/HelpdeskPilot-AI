from app.main import ROOT_DIR
from chromadb import PersistentClient
from pathlib import Path

VECTOR_DB_PATH = ROOT_DIR / 'knowledge_base.db'
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

# Split document lines into chunks with metadata
def chunk_documents(documents) -> list:
    chunks = []
    chunk_index = 0
    for document in documents:
        for line in document['contents'].splitlines():
            if not line:
                continue
            chunks.append(
                {
                    'metadata': {
                        'source': document['filename'],
                        'chunk_index': chunk_index
                    },
                    'text': line
                }
            )
            chunk_index += 1
        chunk_index = 0

    return chunks

def create_collection():
    documents = load_documents()
    chunks = chunk_documents(documents)
    chroma_client = PersistentClient(path=VECTOR_DB_PATH)
    collection = chroma_client.get_or_create_collection(name="knowledge_base")

    ids = [
        f'{chunk['metadata']['source'].removesuffix('.md')}_{chunk['metadata']['chunk_index']}' 
        for chunk in chunks
        ]
    documents = [chunk['text'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    return collection