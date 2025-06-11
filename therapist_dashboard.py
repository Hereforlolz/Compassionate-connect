# therapist_dashboard.py

import json
import os
from insight_agent import InsightAgent

def load_summaries(file_path="summaries.json"):
    print("📁 Loading summaries from:", file_path)

    if not os.path.exists(file_path):
        print("❌ summaries.json file not found.")
        return {}

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} entries.")
            return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return {}

def display_therapist_dashboard():
    print("\n👩‍⚕️ THERAPIST DASHBOARD - CompassionateConnect AI\n" + "-" * 60)

    summaries = load_summaries()
    if not summaries:
        print("⚠️ No summaries found. Check JSON file format.")
        return

    insight_agent = InsightAgent()

    for name, data in summaries.items():
        print(f"\n🧾 Client: {name}")

        # Show timestamp
        timestamp = data.get("timestamp", "No timestamp available.")
        print(f"⏰ Submitted: {timestamp}")

        # Show summary
        summary_text = data.get("summary", "No summary provided.")
        print(f"\n📝 Summary:\n{summary_text}")

        # Generate insights
        print("\n💡 Generating Insights with Gemini...")
        insights = insight_agent.generate_insights(summary_text)
        print(f"\n🔍 Insights:\n{insights}")
        print("\n" + "-" * 60)

if __name__ == "__main__":
    print("👀 Starting Therapist Dashboard...")
    display_therapist_dashboard()
