from utils.common import spin_chapter, review_chapter, human_loop

if __name__ == "__main__":
    # Step 1: Scrape
    chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    chapter_id = "book1_chapter1"
    # scrape_chapter(chapter_url, chapter_id)
    spin_chapter(chapter_id, "v1")
    review_chapter(chapter_id, "v1")
    human_loop(chapter_id, "v1")