import gradio as gr
from utils.scrapper import scrape_chapter
from utils.common import spin_chapter, review_chapter, edit_chapter
from storage.chroma_storage import get_version_text, add_raw_text, get_version_review
from utils.versioning import get_next_version

# --- Logic Functions ---
def handle_url_scrape(url, chapter_id):
    try:
        scrape_chapter(url, chapter_id)
        version_id = get_next_version(chapter_id)
        spin_chapter(chapter_id, version_id)
        review_chapter(chapter_id, version_id)
        return f"Scraped, Spun, and Reviewed successfully as version: {version_id}"
    except Exception as e:
        return f"Error: {str(e)}"

def handle_text_upload(file, chapter_id):
    try:
        raw_text = file.read().decode("utf-8")
        add_raw_text(chapter_id, raw_text)
        version_id = get_next_version(chapter_id)
        spin_chapter(chapter_id, version_id)
        review_chapter(chapter_id, version_id)
        return f"Text uploaded, Spun, and Reviewed successfully as version: {version_id}"
    except Exception as e:
        return f"Error: {str(e)}"

def fetch_version(chapter_id, version_id, stage):
    try:
        return get_version_text(chapter_id, version_id, stage)
    except Exception as e:
        return f"Error: {str(e)}"

def fetch_review(chapter_id, version_id, stage):
    try:
        return get_version_review(chapter_id, version_id, stage)
    except Exception as e:
        return f"Error: {str(e)}"

def hitl_review(chapter_id, version_id, final_text, decision, editor, notes):
    try:
        if decision == "accept":
            stage = "final"
        elif decision == "edit":
            stage = "human_edited"
        elif decision == "retry":
            next_version = get_next_version(chapter_id)
            spin_chapter(chapter_id, next_version)
            review_chapter(chapter_id, next_version)
            edit_chapter(chapter_id, next_version, "ai_reviewed")
            return f"Retrying with version: {next_version}"
        else:
            return "Invalid decision."

        human_review_note = notes or ""
        metadata = {"review": human_review_note, "editor": editor, "timestamp": ""}  # Time optional here
        from storage.chroma_storage import add_version
        add_version(chapter_id, version_id, stage, final_text, review=human_review_note)
        return f"{stage} version added successfully"

    except Exception as e:
        return f"Error: {str(e)}"

def edit_with_ai(chapter_id, version_id, stage):
    try:
        edit_chapter(chapter_id, version_id, stage)
        return f"AI-based edit completed for version {version_id}"
    except Exception as e:
        return f"AI Edit Error: {str(e)}"

# --- Gradio Interface ---
with gr.Blocks() as demo:
    gr.Markdown("# 📚 Chapter Processing System")

    with gr.Tab("1. Scrape from URL"):
        with gr.Row():
            url = gr.Textbox(label="Chapter URL")
            chapter_id_url = gr.Textbox(label="Chapter ID")
        scrape_btn = gr.Button("Scrape and Process")
        scrape_output = gr.Textbox(label="Status")
        scrape_btn.click(fn=handle_url_scrape, inputs=[url, chapter_id_url], outputs=scrape_output)

    with gr.Tab("2. Upload Raw Text"):
        with gr.Row():
            file = gr.File(label="Upload Text File")
            chapter_id_file = gr.Textbox(label="Chapter ID")
        upload_btn = gr.Button("Upload and Process")
        upload_output = gr.Textbox(label="Status")
        upload_btn.click(fn=handle_text_upload, inputs=[file, chapter_id_file], outputs=upload_output)

    with gr.Tab("3. Fetch & Edit Version"):
        with gr.Row():
            fetch_chapter = gr.Textbox(label="Chapter ID")
            fetch_version_id = gr.Textbox(label="Version ID")
            fetch_stage = gr.Dropdown(choices=["raw", "spun", "ai_reviewed", "ai_edited", "human_edited", "final"], value="spun", label="Stage")
        fetch_btn = gr.Button("Fetch Version")
        fetched_text = gr.Textbox(label="Fetched Text (Editable)", lines=20)
        fetched_review = gr.Textbox(label="Fetched Review", lines=7)
        fetch_btn.click(fn=fetch_version, inputs=[fetch_chapter, fetch_version_id, fetch_stage], outputs=fetched_text)
        fetch_btn.click(fn = fetch_review, inputs=[fetch_chapter, fetch_version_id, fetch_stage], outputs=fetched_review)

        gr.Markdown("## Human Feedback")
        decision = gr.Radio(choices=["accept", "edit", "retry"], label="Decision")
        editor = gr.Textbox(label="Your Name/Initials")
        notes = gr.Textbox(label="Review Notes")
        submit_btn = gr.Button("Submit Review")
        review_status = gr.Textbox(label="Status")
        submit_btn.click(fn=hitl_review, inputs=[fetch_chapter, fetch_version_id, fetched_text, decision, editor, notes], outputs=review_status)

        gr.Markdown("## Edit with AI")
        ai_edit_btn = gr.Button("Run AI Editor")
        ai_edit_output = gr.Textbox(label="AI Edit Status")
        ai_edit_btn.click(fn=edit_with_ai, inputs=[fetch_chapter, fetch_version_id, fetch_stage], outputs=ai_edit_output)
if __name__ == "__main__":
    demo.launch()
