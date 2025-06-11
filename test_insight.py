# test_insight.py

from insight_agent import InsightAgent
import json

with open("summaries.json", "r") as f:
    summaries = json.load(f)
    latest_summary = summaries[-1]["summary"]

agent = InsightAgent()
insight = agent.generate_insights(latest_summary)

print("\n🧠 AI-Supported Therapist Insight:\n")
print(insight)
