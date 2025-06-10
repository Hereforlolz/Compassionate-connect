# intake_agent.py
import os
from google.cloud import aiplatform
import google.generativeai as genai

class IntakeQuestionnaireAgent:
    def __init__(self, project_id):
        self.project_id = project_id
        self.location = "us-central1"
        aiplatform.init(project=project_id, location=self.location)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.patient_data = {}
        self.questions = [
            {"id": "name", "question": "What is your full name?", "type": "text", "required": True},
            {"id": "age", "question": "What is your age?", "type": "number", "required": True},
            {"id": "phone", "question": "What is your phone number?", "type": "text", "required": True},
            {"id": "emergency_contact", "question": "Who should we contact in case of emergency? (Name and phone number)", "type": "text", "required": True},
            {"id": "current_mood", "question": "On a scale of 1-10, how would you rate your mood today? (1 = very low, 10 = excellent)", "type": "scale", "required": True},
            {"id": "sleep_pattern", "question": "How has your sleep been lately? (Good/Fair/Poor)", "type": "choice", "required": True},
            {"id": "main_concern", "question": "What brings you to seek mental health support today?", "type": "text", "required": True},
            {"id": "crisis_check", "question": "Are you currently having thoughts of hurting yourself or others? (Yes/No)", "type": "yes_no", "required": True, "crisis_trigger": True}
        ]
        self.current_question_index = 0
        print("📋 IntakeQuestionnaireAgent initialized!")

    def start_intake(self):
        print("""
        📋 Patient Intake Questionnaire

        Welcome! 
        I'll now ask you some questions to help your care team understand your needs better.

        • Please answer as honestly as you feel comfortable
        • If you need clarification on any question, just ask
        • You can say 'skip' if you're not ready to answer something
        • If you're in crisis, I'll immediately connect you with help

        Let's begin:
        """)
        return self.ask_next_question()

    def ask_next_question(self):
        if self.current_question_index >= len(self.questions):
            return self.complete_intake()
        question = self.questions[self.current_question_index]
        print(f"\n❓ Question {self.current_question_index + 1}/{len(self.questions)}:\n{question['question']}")
        return question

    def process_response(self, response, question):
        response = response.strip()
        if question.get('crisis_trigger', False) and self.detect_crisis(response):
            return {"type": "crisis", "response": response}
        if response.lower() in ['skip', 'pass', 'next']:
            if question.get('required', False):
                print("⚠️  This question is required. Let me help clarify it.")
                return self.clarify_question(question)
            else:
                print("📝 Skipped.")
                return self.move_to_next_question()
        if self.validate_response(response, question):
            self.patient_data[question['id']] = response
            print("✅ Thank you!")
            return self.move_to_next_question()
        else:
            print("🤔 Let's clarify that question.")
            return self.clarify_question(question)

    def validate_response(self, response, question):
        if not response:
            return False
        qtype = question.get('type', 'text')
        if qtype == 'number':
            try: return 1 <= int(response) <= 120
            except: return False
        elif qtype == 'scale':
            try: return 1 <= int(response) <= 10
            except: return False
        elif qtype == 'choice':
            return response.lower() in ['good', 'fair', 'poor']
        elif qtype == 'yes_no':
            return response.lower() in ['yes', 'no', 'y', 'n']
        return True

    def clarify_question(self, question):
        prompt = f"""
        A patient is confused by this question: "{question['question']}"
        Provide a kind, brief clarification that:
        - Explains the intent
        - Gives examples
        - Reassures the patient
        """
        try:
            clarification = self.model.generate_content(prompt).text
            print(f"💡 {clarification}")
            return {"type": "clarification", "question": question}
        except:
            print("💡 " + self.get_simple_clarification(question))
            return {"type": "clarification", "question": question}

    def get_simple_clarification(self, question):
        fallback = {
            "name": "Please enter your full name.",
            "age": "Enter your age as a number (e.g., 30).",
            "phone": "Enter a phone number where we can contact you.",
            "emergency_contact": "Provide the name and number of someone we can contact in emergencies.",
            "current_mood": "Rate your mood from 1 (very low) to 10 (excellent).",
            "sleep_pattern": "Choose from Good, Fair, or Poor.",
            "main_concern": "Briefly describe why you're seeking support.",
            "crisis_check": "Please answer Yes or No. This helps us ensure your safety."
        }
        return fallback.get(question['id'], "Please answer as best you can.")

    def detect_crisis(self, response):
        crisis_terms = ['yes', 'y', 'suicide', 'kill', 'hurt', 'harm', 'die', 'end it']
        return any(term in response.lower() for term in crisis_terms)

    def move_to_next_question(self):
        self.current_question_index += 1
        return self.ask_next_question()

    def complete_intake(self):
        print("""
        🎉 Intake Complete!

        Thank you for sharing this information.
        A professional will review your responses and reach out within 24–48 hours.
        If you're in immediate danger, please call 911.
        💚 You've taken an important step!
        """)
        return {"type": "completed", "data": self.patient_data}


def test_intake_agent():
    print("Testing IntakeQuestionnaireAgent...")
    project_id = "compassionate-connect-ai"
    try:
        agent = IntakeQuestionnaireAgent(project_id)
        question = agent.start_intake()
        while True:
            if isinstance(question, dict) and question.get('type') == 'completed':
                print("\n📋 Final Data:")
                for k, v in question['data'].items():
                    print(f"  {k}: {v}")
                break
            elif question.get('type') == 'crisis':
                print("\n🚨 CRISIS DETECTED — Immediate help needed!")
                break
            user_input = input("\nYour answer: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("Exiting...")
                break
            if question.get('type') == 'clarification':
                question = question['question']
            result = agent.process_response(user_input, question)
            if result.get('type') == 'crisis':
                print("\n🚨 CRISIS DETECTED — Immediate help needed!")
                break
            elif result.get('type') == 'completed':
                print("\n📋 Final Data:")
                for k, v in result['data'].items():
                    print(f"  {k}: {v}")
                break
            question = result
    except Exception as e:
        print(f"❌ Error: {e}\nPlease check your Google Cloud project settings.")

if __name__ == "__main__":
    test_intake_agent()
