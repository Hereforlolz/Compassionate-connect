# therapist_dashboard.py

import json
import os
from datetime import datetime
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

def save_summaries(summaries, file_path="summaries.json"):
    try:
        with open(file_path, "w") as f:
            json.dump(summaries, f, indent=4)
        print("💾 summaries.json updated with insights.")
    except Exception as e:
        print(f"❌ Failed to save summaries: {e}")

def display_therapist_dashboard():
    print("\n👩‍⚕️ THERAPIST DASHBOARD - CompassionateConnect AI\n" + "-" * 60)

    summaries = load_summaries()
    if not summaries:
        print("⚠️ No summaries found. Check JSON file format.")
        return

    insight_agent = InsightAgent()

    updated = False  # Flag to avoid saving if nothing changed

    for name, data in summaries.items():
        print(f"\n🧾 Client: {name}")
        timestamp = data.get("timestamp", "No timestamp available.")
        print(f"⏰ Submitted: {timestamp}")

        summary_text = data.get("summary", "No summary provided.")
        print(f"\n📝 Summary:\n{summary_text}")

        if "insights" in data:
            print("\n📌 Previously Generated Insights:\n" + data["insights"])
        else:
            print("\n💡 Generating Insights with Gemini...")
            insights = insight_agent.generate_insights(summary_text)
            print(f"\n🔍 Insights:\n{insights}")

            # Save insights into summary
            data["insights"] = insights
            data["insights_generated_at"] = datetime.now().isoformat()
            updated = True

        print("\n" + "-" * 60)

    if updated:
        save_summaries(summaries)

if __name__ == "__main__":
    print("👀 Starting Therapist Dashboard...")
    display_therapist_dashboard()
