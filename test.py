# test.py
from intake_agent import IntakeQuestionnaireAgent

project_id = "your-gcp-project-id"  # Replace with your actual GCP project ID

agent = IntakeQuestionnaireAgent(project_id=project_id)
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
        print("👋 Exiting the intake process.")
        break

    if question.get('type') == 'clarification':
        question = question['question']

    result = agent.process_response(user_input, question)

    if result.get('type') == 'completed':
        print("\n📋 Final Data:")
        for k, v in result['data'].items():
            print(f"  {k}: {v}")
        break
    elif result.get('type') == 'crisis':
        print("\n🚨 CRISIS DETECTED — Immediate help needed!")
        break

    question = result
