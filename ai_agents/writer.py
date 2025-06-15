from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq = Groq()
GROQ_MODEL = "llama3-70b-8192"

class WriterAgent:
    def __init__(self, model_name=GROQ_MODEL):
        self.model = model_name
        print(f"⚡ Using Groq model: {self.model}")

    def spin_text(self, input_text: str, prompt_style="modern rewrite") -> str:
        prompt = f"Rewrite the following passage in a {prompt_style} style:\n\n{input_text}"

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
