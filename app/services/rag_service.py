from app.main import DOCUMENTS

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
                    'source': document['filename'],
                    'chunk_index': chunk_index,
                    'chunk': line,
                }
            )
            chunk_index += 1
        chunk_index = 0
        
    return chunks