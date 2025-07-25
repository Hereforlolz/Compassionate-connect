# crisis_response_agent.py
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

class CrisisResponseAgent:
    def __init__(self, project_id):
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def handle_crisis(self, user_input):
        prompt = f"""
        A patient has indicated a crisis in their intake form:
        "{user_input}"
        
        Please respond empathetically and recommend they call a crisis line (e.g., 988).
        Keep it short, supportive, and calming.
        """
        try:
            response = self.model.generate_content(prompt)
            print(f"\n💬 AI Response:\n{response.text}")
            print("\n📟 (Simulated alert sent to clinic staff.)")
        except Exception:
            print("⚠️ Crisis detected. Please call 911 or go to the nearest emergency room.")
