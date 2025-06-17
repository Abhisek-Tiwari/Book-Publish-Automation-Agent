from datetime import datetime
from storage.chroma_storage import get_version_text

def human_review(chapter_id: str, version_id: str):
    try:
        spun_text = get_version_text(chapter_id, version_id, "spun")
        review_text = get_version_text(chapter_id, version_id, "ai_reviewed")
    except ValueError as e:
        print(f"Error: {e}")
        return None

    print("\n--- Spun Chapter Text ---")
    print(spun_text)
    print("\n --- AI Review ---")
    print(review_text)

    print("\nOptions:")
    print("1. Accept as-is")
    print("2. Edit manually")
    print("3. Reject and retry rewrite")

    choice = input("\nYour decision (1/2/3): ").strip()

    editor_name = input("Enter your name or initials: ").strip()

    human_notes = input("\nOptional: Add your review notes (press Enter to skip): ")

    result = {
        "status": "",
        "final_text": "",
        "human_review": human_notes,
        "editor": editor_name,
        "timestamp": datetime.now().isoformat()
    }

    if choice == "1":
        result["status"] = "accepted"
        result["final_text"] = spun_text

    elif choice == "2":
        print("Enter your manual edits. Type 'END' on a new line when done.")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        result["status"] = "edited"
        result["final_text"] = "\n".join(lines)

    elif choice == "3":
        result["status"] = "retry"
        result["final_text"] = None

    else:
        print("Invalid choice.")
        return None

    return result