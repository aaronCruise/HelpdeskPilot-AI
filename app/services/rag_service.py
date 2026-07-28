from app.main import DOCUMENTS
from chromadb import Client

# Split document lines into chunks with metadata
def chunk_documents(documents=DOCUMENTS) -> list:
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

# TODO: possibly persistent memory for db
def create_collection():
    chunks = chunk_documents()
    chroma_client = Client()
    collection = chroma_client.create_collection(name="knowledge_base")

    ids = [
        f'{chunk['metadata']['source'].removesuffix('.md')}_{chunk['metadata']['chunk_index']}' 
        for chunk in chunks
        ]
    documents = [chunk['text'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    return collection