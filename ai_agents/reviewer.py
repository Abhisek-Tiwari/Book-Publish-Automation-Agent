from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq = Groq()
GROQ_MODEL = "llama3-70b-8192"

class ReviewerAgent:
    def __init__(self, model_name=GROQ_MODEL):
        self.model = model_name
        print(f"Using Groq model for review: {self.model}")

    def review(self, original: str, rewritten: str) -> str:
        system_prompt = "You are a detailed literary reviewer. Compare the rewritten passage to the original, and provide constructive feedback."

        prompt = f"""You are a detailed literary reviewer. Compare the rewritten passage to the original, and provide constructive feedback.

        ### Original Passage:
        {original}
        
        ### Rewritten Passage:
        {rewritten}
        
        ### Review Instructions:
        Critically assess the rewritten version for:
        - Clarity and flow
        - Preservation of meaning
        - Tone and style shifts
        - Suggestions for improvement
        
        Output in clear bullet points or paragraphs.
        """

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