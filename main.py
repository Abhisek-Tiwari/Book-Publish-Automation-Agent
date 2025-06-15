from ai_agents.reviewer import ReviewerAgent
import os

def review_chapter(chapter_id: str):
    input_path = f"data/raw/{chapter_id}.txt"
    spun_path = f"data/versions/{chapter_id}_spun.txt"
    review_path = f"data/reviews/{chapter_id}_review.txt"

    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    with open(spun_path, "r", encoding="utf-8") as f:
        rewritten_text = f.read()

    reviewer = ReviewerAgent()
    feedback = reviewer.review(original_text, rewritten_text)

    with open(review_path, "w", encoding="utf-8") as f:
        f.write(feedback)

    print(f"📝 Review saved to: {review_path}")

from storage.chroma_storage import add_version

def save_to_chroma(chapter_id: str):
    raw_path = f"data/raw/{chapter_id}.txt"
    spun_path = f"data/versions/{chapter_id}_spun.txt"
    review_path = f"data/reviews/{chapter_id}_review.txt"

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    print(raw_text)
    with open(spun_path, "r", encoding="utf-8") as f:
        spun_text = f.read()
    print(spun_text)
    with open(review_path, "r", encoding="utf-8") as f:
        review_text = f.read()
    print(review_text)
    add_version(chapter_id, version_id="v1", stage="raw", text=raw_text, review= "")
    add_version(chapter_id, version_id="v1", stage="ai_spun", text=spun_text, review = "")
    add_version(chapter_id, version_id="v1", stage="ai_reviewed", text=spun_text, review=review_text)

from interface.human_editor_cli import human_review

def human_loop(chapter_id: str, version_id="v1"):
    result = human_review(chapter_id)

    if not result:
        return

    if result["status"] == "accepted":
        add_version(chapter_id, version_id, "final", result["final_text"], "")

    elif result["status"] == "edited":
        add_version(chapter_id, version_id, "human_edited", result["final_text"], "")
        add_version(chapter_id, version_id, "final", result["final_text"], "")

    elif result["status"] == "retry":
        print("You can now re-run the spin + review steps for a new version.")

if __name__ == "__main__":
    # Step 1: Scrape
    chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    chapter_id = "book1_chapter1"
    # scrape_chapter(chapter_url, chapter_id)
    human_loop(chapter_id)