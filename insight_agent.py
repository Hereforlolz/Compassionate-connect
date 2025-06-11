# insight_agent.py

import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")  # Replace with your actual key

class InsightAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_insights(self, summary_text):
        prompt = f"""
        You are a clinical assistant AI supporting mental health professionals.

        Based on the following patient summary, list:
        1. Possible areas of concern (e.g., trauma, anxiety, burnout, depression)
        2. Potential therapy approaches that may help (e.g., CBT, trauma-informed, ACT, mindfulness-based)
        3. A disclaimer that these are suggestions, not diagnoses.

        Avoid making firm clinical judgments.

        Summary:
        {summary_text}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Error generating insights: {e}"
