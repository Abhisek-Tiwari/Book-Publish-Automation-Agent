import chromadb
from chromadb.utils import embedding_functions

chroma_path = "data/chroma_db"

client = chromadb.PersistentClient(path=chroma_path)

embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name = "all-MiniLM-L6-v2")

collection = client.get_or_create_collection(
    name = "chapter_versions",
    embedding_function = embed_func
)

def add_version(chapter_id: str, version_id: str, stage: str, text: str, review: str):
    doc_id = f"{chapter_id}_{version_id}_{stage}"

    metadata = {
        chapter_id: chapter_id,
        version_id: version_id,
        stage: stage,
        review: review,
    }

    collection.add(
        documents = [text],
        metadatas = [metadata],
        ids = [doc_id],
    )

    print(f"Chapter Version: {chapter_id}/{version_id}/{stage} added successfully")


def query_similar(text, top_k=3):
    return collection.query(query_texts=[text], n_results=top_k)