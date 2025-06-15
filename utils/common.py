from ai_agents.writer import WriterAgent
from ai_agents.reviewer import ReviewerAgent
from storage.chroma_storage import add_version
from interface.human_editor_cli import human_review
from utils.versioning import get_next_version

def spin_chapter(chapter_id: str, version_id: str):
    input_path = f"data/raw/{chapter_id}.txt"
    output_path = f"data/versions/{chapter_id}_{version_id}_spun.txt"

    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    writer = WriterAgent()
    spun = writer.spin_text(original_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(spun)

    print(f"Spun version saved to: {output_path}")



def review_chapter(chapter_id: str, version_id: str):
    input_path = f"data/raw/{chapter_id}.txt"
    spun_path = f"data/versions/{chapter_id}_{version_id}_spun.txt"
    review_path = f"data/reviews/{chapter_id}_{version_id}_review.txt"

    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    with open(spun_path, "r", encoding="utf-8") as f:
        rewritten_text = f.read()

    reviewer = ReviewerAgent()
    feedback = reviewer.review(original_text, rewritten_text)

    with open(review_path, "w", encoding="utf-8") as f:
        f.write(feedback)

    print(f"Review saved to: {review_path}")



def human_loop(chapter_id: str, version_id: str):
    next_version = get_next_version(chapter_id)
    result = human_review(chapter_id, version_id)

    if not result:
        return

    metadata = {
        "review": result.get("human_review", ""),
        "editor": result.get("editor", "unknown"),
        "timestamp": result.get("timestamp", ""),
    }

    if result["status"] == "accepted":
        add_version(chapter_id, version_id, "final", result["final_text"], review=metadata["review"])

    elif result["status"] == "edited":
        add_version(chapter_id, next_version, "human_edited", result["final_text"], review=metadata["review"])
        add_version(chapter_id, next_version, "final", result["final_text"], review=metadata["review"])

    elif result["status"] == "retry":
        print(f"Spinning next version: {next_version}")
        spin_chapter(chapter_id, next_version)
