#test_intake_agent
from intake_agent import IntakeQuestionnaireAgent

# Replace with your actual project ID
PROJECT_ID = "compassionate-connect-ai"

# Simulate user session
agent = IntakeQuestionnaireAgent(project_id=PROJECT_ID)

# Manually set fake answers
agent.patient_data = {
    "name": "Jamie",
    "phone": "1234567890"
}

# TEST CASE 1: Crisis answer
print(">>> Testing crisis detection with 'yes'")
agent.detect_crisis("yes")
