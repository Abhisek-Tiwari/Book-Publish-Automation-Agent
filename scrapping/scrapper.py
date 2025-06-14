from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

def scrape_chapter(url: str, chapter_id: str):
    """
    Scrapes text from any chapter and saves screenshots
    :param url: Url of chapter to be read
    :param chapter_id: Chapter ID of chapter to be read
    :return:
    """
    screenshot_path = f"data/screenshots/{chapter_id}.png"
    text_path = f"data/raw/{chapter_id}.txt"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        page.screenshot(path = screenshot_path, full_page = True)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", class_="mw-parser-output")
    paragraphs = content_div.find_all("p") if content_div else []
    text = "\n\n".join([p.getText().strip() for p in paragraphs if p.getText(strip=True)])

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Scraping of {chapter_id} is successful")
