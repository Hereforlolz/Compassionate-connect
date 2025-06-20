import os
import json
from datetime import datetime, timedelta
import google.generativeai as genai
from google.cloud import firestore

class IntakeQuestionnaireAgent:
    def __init__(self, project_id):
        self.project_id = project_id
        self.location = "us-central1"

        # === Added this line to fix the AttributeError ===
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("GENAI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.patient_data = {}
        self.questions = [
            {"id": "name", "question": "What is your full name?", "type": "text", "required": True},
            {"id": "age", "question": "What is your age?", "type": "number", "required": True},
            {"id": "phone", "question": "What is your phone number?", "type": "text", "required": True},
            {"id": "emergency_contact", "question": "Who should we contact in case of emergency? (Name and phone number)", "type": "text", "required": True},
            {"id": "current_mood", "question": "On a scale of 1-10, how would you rate your mood today?", "type": "scale", "required": True},
            {"id": "sleep_pattern", "question": "How has your sleep been lately? (Good/Fair/Poor)", "type": "choice", "required": True},
            {"id": "main_concern", "question": "What brings you to seek mental health support today?", "type": "text", "required": True},
            {"id": "crisis_check", "question": "Are you currently having thoughts of hurting yourself or others? (Yes/No)", "type": "yes_no", "required": True, "crisis_trigger": True}
        ]
        self.current_question_index = 0
        print("✓ IntakeQuestionnaireAgent initialized!")

    def start_intake(self):
        print("""
        Patient Intake Questionnaire

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
        self.patient_data[question['id']] = response  # 🔑 Store before checking crisis

        if question.get('crisis_trigger', False) and self.detect_crisis(response):
            return {"type": "crisis", "response": response}

        if response.lower() in ['skip', 'pass', 'next']:
            if question.get('required', False):
                print("This question is required. Let me help clarify it.")
                return self.clarify_question(question)
            else:
                print("Skipped.")
                return self.move_to_next_question()

        if self.validate_response(response, question):
            print(" Thank you!")
            return self.move_to_next_question()
        else:
            print(" Let's clarify that question.")
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
            print(f"{clarification}")
            return {"type": "clarification", "question": question}
        except:
            print(" " + self.get_simple_clarification(question))
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
        crisis_terms = ['yes', 'y', 'suicide', 'kill', 'hurt', 'harm', 'die', 'end it', "depressed", "tired of it", "giving up", "give up"]
        is_crisis = any(term in response.lower() for term in crisis_terms)
        if is_crisis:
            print("🫂")
            self.patient_data['crisis_detected'] = True
            self.patient_data['crisis_timestamp'] = datetime.now().isoformat()
            self.log_crisis_flag()
            self.log_crisis_followup()
        return is_crisis

    def log_crisis_flag(self):
        try:
            db = firestore.Client(project=self.project_id)
            crisis_entry = {
                "user_id": self.patient_data.get("phone", "unknown"),
                "name": self.patient_data.get("name", "Unknown"),
                "timestamp": datetime.utcnow()
            }
            db.collection("crisis_flags").add(crisis_entry)
            print(f"🚨 Crisis flag logged: {crisis_entry}")
        except Exception as e:
            print(f"⚠️ Failed to log crisis flag: {e}")

    def log_crisis_followup(self):
        name = self.patient_data.get("name", "Unknown")
        timestamp = datetime.now().isoformat()
        message = (
            f"Hi {name}, just checking in after yesterday. "
            "How are you feeling today? Would you like to schedule a session?"
        )
        followup_entry = {
            "name": name,
            "timestamp": timestamp,
            "message": message
        }

        log_path = "follow_up_log.json"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(followup_entry)

        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        try:
            db = firestore.Client(project=self.project_id)
            db.collection("crisis_followups").add(followup_entry)
            print("📬 Follow-up logged successfully.")
        except Exception as e:
            print(f"⚠️ Error logging follow-up to Firestore: {e}")

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

    def run(self):
        question = self.start_intake()
        while True:
            if isinstance(question, dict) and question.get('type') == 'completed':
                print("\n Final Data:")
                for k, v in question['data'].items():
                    print(f"  {k}: {v}")
                break
            elif question.get('type') == 'crisis':
                print("\n CRISIS DETECTED — Please reach out to 911 or your loved ones for Immediate help!")
                print("✅ Crisis response handled and logged.")
                break
            user_input = input("\nYour answer: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("Exiting...")
                break
            if question.get('type') == 'clarification':
                question = question['question']
            result = self.process_response(user_input, question)
            if result.get('type') == 'crisis':
                print("\n 🫂🫂Sorry you feel this way. — Please reach out to 911 or your loved ones for Immediate help!")
                break
            elif result.get('type') == 'completed':
                print("\nFinal Data:")
                for k, v in result['data'].items():
                    print(f"  {k}: {v}")
                break
            question = result

    def process_form_submission(self, form_data: dict):
        """
        New method to process a complete form submission in one call (for web/API use).
        Does NOT change existing interactive CLI logic.
        """

        # 1) Store incoming form data
        self.patient_data = form_data

        # 2) Check crisis triggers
        crisis_flagged = False
        for q in self.questions:
            if q.get('crisis_trigger', False):
                response = form_data.get(q['id'], "")
                if self.detect_crisis(response):
                    crisis_flagged = True

        # 3) Save to Firestore
        try:
            db = firestore.Client(project=self.project_id)
            db.collection("intake_submissions").add(self.patient_data)
            print("✅ Intake form saved to Firestore.")
        except Exception as e:
            print(f"⚠️ Firestore save error: {e}")

        # 4) Save to summaries.json as record
        try:
            with open("summaries.json", "a") as f:
                f.write(json.dumps(self.patient_data) + "\n")
            print("🗂️ Saved to summaries.json.")
        except Exception as e:
            print(f"⚠️ Could not write to summaries.json: {e}")

        # 5) Generate short text summary
        summary = (
            f"Patient {form_data.get('name', 'Unknown')} "
            f"reported mood {form_data.get('current_mood', '?')}, "
            f"sleep pattern {form_data.get('sleep_pattern', '?')}, "
            f"and main concern: {form_data.get('main_concern', '')}."
        )

        return {
            "summary": summary,
            "crisis_flagged": crisis_flagged
        }

