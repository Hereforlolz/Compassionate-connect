from intake_agent import IntakeQuestionnaireAgent
from crisis_response_agent import CrisisResponseAgent
from summary_generator_agent import SummaryGeneratorAgent
from data_persistence_agent import DataPersistenceAgent
import time

class OnboardingCoordinatorAgent:
    def __init__(self, project_id):
        self.intake_agent = IntakeQuestionnaireAgent(project_id)
        self.crisis_agent = CrisisResponseAgent(project_id)
        self.summary_agent = SummaryGeneratorAgent(project_id)
        self.storage_agent = DataPersistenceAgent(project_id)

    def run(self):
        print("\n👋 Welcome to CompassionateConnect AI — Mental Health Intake System")
        print("We’ll walk you through a few questions to help us support you.")
        time.sleep(1)

        current_question = self.intake_agent.start_intake()

        while True:
            if current_question.get('type') == 'completed':
                data = current_question['data']

                print("\n📋 Final Data:")
                for k, v in data.items():
                    print(f"  {k}: {v}")

                confirmation = input("\n🛑 Is the information above correct? Type 'y' to confirm and save: ").strip().lower()
                if confirmation == 'y':
                    self.storage_agent.save_data(data)
                    summary = self.summary_agent.generate_summary(data)
                    self.storage_agent.save_summary_to_json(summary)
                    print("\n✅ Intake complete. Your information has been recorded.")
                else:
                    print("📝 Let's make some updates to your answers.")
                    keys = list(data.keys())
                    while True:
                        print("\nWhich field would you like to update?")
                        for i, key in enumerate(keys, 1):
                            print(f"{i}. {key}: {data[key]}")
                        choice = input("Type number to edit or 'done' to finish: ").strip().lower()
                        if choice == 'done':
                            break
                        if choice.isdigit() and 1 <= int(choice) <= len(keys):
                            field = keys[int(choice)-1]
                            new_value = input(f"Enter new value for '{field}': ")
                            data[field] = new_value
                        else:
                            print("❌ Invalid choice.")

                    # Show final version and ask again
                    print("\nUpdated Final Data:")
                    for k, v in data.items():
                        print(f"  {k}: {v}")
                    reconfirm = input("Type 'y' to confirm and save: ").strip().lower()
                    if reconfirm == 'y':
                        self.storage_agent.save_data(data)
                        summary = self.summary_agent.generate_summary(data)
                        self.storage_agent.save_summary_to_json(summary)
                        print("\n✅ Updated intake saved.")
                    else:
                        print("❌ Intake not confirmed. Data was not saved.")
                break

            elif current_question.get('type') == 'crisis':
                user_message = current_question['response']
                self.crisis_agent.handle_crisis(user_message)
                break

            elif current_question.get('type') == 'clarification':
                current_question = current_question['question']

            else:
                response = input("\nYour response: ")
                current_question = self.intake_agent.process_response(response, current_question)

if __name__ == "__main__":
    coordinator = OnboardingCoordinatorAgent(project_id="compassionate-connect-ai")
    coordinator.run()
