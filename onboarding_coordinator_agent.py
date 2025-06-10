# onboarding_coordinator_agent.py
from intake_agent import IntakeQuestionnaireAgent
from crisis_response_agent import CrisisResponseAgent
from data_persistence_agent import DataPersistenceAgent
from summary_generator_agent import SummaryGeneratorAgent
import google.generativeai as genai

class OnboardingCoordinatorAgent:
    def __init__(self, project_id, api_key):
        # ✅ Configure the Gemini API
        genai.configure(api_key=api_key)

        self.project_id = project_id
        self.intake_agent = IntakeQuestionnaireAgent(project_id)
        self.crisis_agent = CrisisResponseAgent(project_id)
        self.storage_agent = DataPersistenceAgent(project_id)
        self.summary_agent = SummaryGeneratorAgent(project_id)

    def run(self):
        current_question = self.intake_agent.start_intake()

        while True:
            if isinstance(current_question, dict):
                if current_question.get('type') == 'completed':
                    data = current_question['data']
                    self.storage_agent.save_data(data)

                    # ✅ Generate summary
                    summary = self.summary_agent.generate_summary(data)
                    print("\n📄 Summary for Care Team/ Clinician:")
                    print(summary)
                    break

                elif current_question.get('type') == 'crisis':
                    self.crisis_agent.handle_crisis(current_question['response'])
                    break

            user_response = input("\nYour answer: ").strip()

            if user_response.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            # ✅ Always pass full question dict to process_response
            if isinstance(current_question, dict) and 'question' in current_question:
                question_dict = current_question
            else:
                # fallback for non-dict inputs
                question_dict = {"type": "text", "question": str(current_question), "id": "unknown", "required": False}

            result = self.intake_agent.process_response(user_response, question_dict)

            # ⏭️ Handle clarification or move to next question
            if isinstance(result, dict) and result.get('type') == 'clarification':
                current_question = result.get('question')
            else:
                current_question = result
