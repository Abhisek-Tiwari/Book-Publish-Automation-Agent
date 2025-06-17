import re
from storage.chroma_storage import get_collection


def get_next_version(chapter_id: str) -> str:
    collection = get_collection()

    results = collection.get(where={"chapter_id": chapter_id})
    version_ids = []

    for metadata in results["metadatas"]:
        version_str = metadata.get("version_id", "")
        match = re.match(r"v(\d+)", version_str)
        if match:
            version_ids.append(int(match.group(1)))

    if not version_ids:
        return "v1"

    max_version = max(version_ids)
    return f"v{max_version + 1}"
