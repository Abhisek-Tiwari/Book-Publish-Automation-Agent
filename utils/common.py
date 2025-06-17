from ai_agents.writer import WriterAgent
from ai_agents.reviewer import ReviewerAgent
from storage.chroma_storage import add_version, get_version_text
from interface.human_editor_cli import human_review
from utils.versioning import get_next_version

def spin_chapter(chapter_id: str, version_id: str):
    raw_text = get_version_text(chapter_id, None, "raw")

    writer = WriterAgent()
    spun = writer.spin_text(raw_text)
    print(f"Text spun successfully with version: {version_id}")

    add_version(chapter_id, version_id, "spun", spun)
    print(f"Spun added to database with version: {version_id}")


def review_chapter(chapter_id: str, version_id: str):
    raw_text = get_version_text(chapter_id, None, "raw")
    spun_text = get_version_text(chapter_id, version_id, "spun")

    reviewer = ReviewerAgent()
    feedback = reviewer.review(raw_text, spun_text)
    print(f"Text reviewed successfully with version: {version_id}")

    spun_text = "\n\nReview by AI:\n"

    add_version(chapter_id, version_id, "ai_reviewed", spun_text, feedback)
    print(f"Review added to database with {version_id}")


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
        add_version(chapter_id, version_id, "human_edited", result["final_text"], review=metadata["review"])

    elif result["status"] == "retry":
        print(f"Spinning next version: {next_version}")
        spin_chapter(chapter_id, next_version)
        print(f"Reviewing next version: {next_version}")
        review_chapter(chapter_id, next_version)