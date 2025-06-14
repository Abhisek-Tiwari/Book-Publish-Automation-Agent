from scrapping.scrapper import scrape_chapter

if __name__ == "__main__":
    chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    chapter_id = "book1_chapter1"
    scrape_chapter(chapter_url, chapter_id)