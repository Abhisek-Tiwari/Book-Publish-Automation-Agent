import argparse
from storage.chroma_storage import get_collection
from chromadb.utils import embedding_functions

embedding_fn = embedding_functions.DefaultEmbeddingFunction()
vector_store = get_collection()

def search_versions(query: str, chapter_id = None, stage = None, k=3):
    filters ={}
    if chapter_id:
        filters["chapter_id"] = chapter_id
    if stage:
        filters["stage"] = stage

    results = vector_store.query(
        query_texts=[query],
        n_results = k,
        filters = filters
    )

    for i, (doc, meta) in enumerate(zip(results["document"][0], results["metadata"][0])):
        print(f"For Result #{i+1}")
        print(f"Chapter: {meta['chapter_id']}")
        print(f"Stage: {meta['stage']}")
        print(f"Text: {doc[:800]}{'...' if len(doc) > 800 else ''}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic search over chapter versions.")
    parser.add_argument("--query", required=True, help="Search phrase")
    parser.add_argument("--chapter", help="Filter by chapter ID (optional)")
    parser.add_argument("--stage", help="raw / ai_spun / ai_reviewed (optional)")
    parser.add_argument("--topk", type=int, default=3, help="How many results to return")

    args = parser.parse_args()
    search_versions(args.query, args.chapter, args.stage, args.topk)