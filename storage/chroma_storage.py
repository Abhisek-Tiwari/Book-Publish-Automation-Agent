import chromadb
from chromadb.utils import embedding_functions

chroma_path = "data/chroma_db"

client = chromadb.PersistentClient(path=chroma_path)

embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name = "all-MiniLM-L6-v2")

collection = client.get_or_create_collection(
    name = "chapter_versions",
    embedding_function = embed_func
)

def add_version(chapter_id: str, version_id: str, stage: str, text: str, review: str = None):
    doc_id = f"{chapter_id}_{version_id}_{stage}"

    metadata = {
        "chapter_id": chapter_id,
        "version_id": version_id,
        "stage": stage,
        "review": review or "",
    }

    collection.upsert(
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id],
    )

    print(f"Chapter Version: {chapter_id}/{version_id}/{stage} added successfully")


def add_raw_text(chapter_id: str, text: str):
    add_version(chapter_id=chapter_id, version_id= "v0", stage="raw", text=text)

def get_version_text(chapter_id: str, version_id: str = None, stage: str = "raw"):
    if version_id:
        doc_id = f"{chapter_id}_{version_id}_{stage}"
    else:
        doc_id = f"{chapter_id}_v0_{stage}"

    result = collection.get(ids=[doc_id])
    if result and result["documents"]:
        return result["documents"][0]
    raise ValueError(f"No version found for {doc_id}")

def get_version_review(chapter_id: str, version_id: str, stage: str):
    if version_id:
        doc_id = f"{chapter_id}_{version_id}_{stage}"
    else:
        doc_id = f"{chapter_id}_v0_{stage}"

    result = collection.get(ids=[doc_id])
    if result and result["metadatas"]:
        return result["metadatas"][0]["review"]
    raise ValueError(f"No version found for {doc_id}")


def get_collection():
    return collection