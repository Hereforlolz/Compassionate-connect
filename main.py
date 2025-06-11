from intake_agent import IntakeQuestionnaireAgent
from crisis_response_agent import CrisisResponseAgent
from data_persistence_agent import DataPersistenceAgent
from insight_agent import InsightAgent

PROJECT_ID = "compassionate-connect-ai"

if __name__ == "__main__":
    print("\n🌟 Welcome to CompassionateConnect AI")
    intake_agent = IntakeQuestionnaireAgent(PROJECT_ID)
    crisis_agent = CrisisResponseAgent(PROJECT_ID)
    storage_agent = DataPersistenceAgent(PROJECT_ID)
    insight_agent = InsightAgent()

    result = intake_agent.run()

    if result and isinstance(result, dict) and result.get("type") == "completed":
        print("\n✅ Intake completed. Saving data and generating insights...")
        data = result["data"]
        storage_agent.save_data(data)

        # Generate and store summary + insight
        summary = "This patient has reported moderate distress. Further attention recommended."  # Replace with real summary generator
        storage_agent.save_summary_with_data(summary, data)

        insights = insight_agent.generate_insights(summary)
        print("\n🔍 AI-generated insights for therapist:")
        print(insights)

    elif result and result.get("type") == "crisis":
        print("\n🚨 Crisis detected — running crisis response agent.")
        crisis_agent.handle_crisis(result["response"])
