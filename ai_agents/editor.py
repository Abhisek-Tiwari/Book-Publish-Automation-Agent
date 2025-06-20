from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq = Groq()
GROQ_MODEL = "llama3-70b-8192"

class EditorAgent:
    def __init__(self, model_name=GROQ_MODEL):
        self.model = model_name
        print(f"Using Groq model for Editing: {self.model}")

    def edit_text(self, spun_text: str, review_text: str) -> str:
        prompt = f"You are a helpful AI assistant. You are given an Input Text and its corresponding Review, which contains suggestions, corrections, or improvements. Your task is to generate a Rewritten Text by incorporating the feedback from the review. The new version should preserve the original meaning but reflect the improvements mentioned in the review. Output only the rewritten text — no preamble, no summary, and no final remarks. Do not include anything like 'Here is the rewritten text...', 'Sure thing, here's' or 'I hope this...' — just return the clean rewritten passage.\nFormat:\nInput Text:\n{spun_text}\n\nRewritten Text:\n{review_text}"

        chat_completions = groq.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        return chat_completions.choices[0].message.content.strip()