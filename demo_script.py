# demo_script.py

from onboarding_coordinator_agent import OnboardingCoordinatorAgent
import time

# Simulated patient responses (replace or randomize as needed)
demo_responses = [
    "John Doe",            # name
    "29",                  # age
    "555-123-4567",        # phone
    "Jane Doe, 555-987-6543",  # emergency contact
    "4",                   # mood
    "poor",                # sleep
    "I’ve been feeling extremely overwhelmed and hopeless lately",  # concern
    "yes"                  # triggers crisis
]

def run_demo():
    print("\n🎬 Starting Demo: CompassionateConnect AI\n")
    coordinator = OnboardingCoordinatorAgent(project_id="compassionate-connect-ai")

    current_question = coordinator.intake_agent.start_intake()

    for response in demo_responses:
        time.sleep(1)  # Simulate pause
        print(f"\n🧑 Patient: {response}")
        if current_question.get('type') == 'clarification':
            current_question = current_question['question']
        result = coordinator.intake_agent.process_response(response, current_question)

        if result.get('type') == 'crisis':
            print("\n🚨 Crisis Detected. Redirecting to CrisisResponseAgent...")
            coordinator.crisis_agent.handle_crisis(response)
            return
        elif result.get('type') == 'completed':
            print("\n✅ Intake Complete. Saving data + generating summary...")
            data = result['data']
            coordinator.storage_agent.save_data(data)
            summary = coordinator.summary_agent.generate_summary(data)
            coordinator.storage_agent.save_summary_to_json(summary)
            print("\n🩺 Summary stored. Ready for therapist dashboard.")
            return
        current_question = result

if __name__ == "__main__":
    run_demo()
