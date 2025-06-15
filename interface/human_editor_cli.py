import os

def human_review(chapter_id: str):
    spun_path = f"data/versions/{chapter_id}_spun.txt"
    review_path = f"data/reviews/{chapter_id}_review.txt"

    if not os.path.exists(spun_path) or not os.path.exists(review_path):
        print("Spun or review file not found.")
        return None

    with open(spun_path, "r", encoding="utf-8") as f:
        spun_text = f.read()
    with open(review_path, "r", encoding="utf-8") as f:
        review_text = f.read()

    print("\n--- Spun Chapter Text ---")
    print(spun_text)
    print("\n--- AI Review ---")
    print(review_text)

    print("\nOptions:")
    print("1. Accept as-is")
    print("2. Edit manually")
    print("3. Reject and retry rewrite")

    choice = input("\nYour decision (1/2/3): ").strip()

    if choice == "1":
        print("Accepted.")
        return {"status": "accepted", "final_text": spun_text}

    elif choice == "2":
        print("Enter your manual edits. Type 'END' on a new line when done.")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        edited_text = "\n".join(lines)
        print("Edited version saved.")
        return {"status": "edited", "final_text": edited_text}

    elif choice == "3":
        print("Rewriting suggested.")
        return {"status": "retry", "final_text": None}

    else:
        print("Invalid choice.")
        return None