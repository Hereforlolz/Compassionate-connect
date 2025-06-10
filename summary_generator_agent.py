# summary_generator_agent.py
import google.generativeai as genai

class SummaryGeneratorAgent:
    def __init__(self, project_id):
        self.project_id = project_id
        self.location = "us-central1"
    def __init__(self, project_id=None):  # optional if unused
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    def generate_summary(self, data):
        prompt = f"""
You are a clinical assistant AI. Summarize the patient's intake form clearly for a mental health clinician.
Format:
- Name and age
- Mood and sleep info
- Main concern
- Any crisis risk
- Any pattern you find in their response


Here’s the intake data:
{data}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Failed to generate summary: {e}"
