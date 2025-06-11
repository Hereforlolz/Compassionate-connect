# push_to_firestore.py

import json
import os
from data_persistence_agent import DataPersistenceAgent
from datetime import datetime

project_id = "compassionate-connect-ai"
persistence = DataPersistenceAgent(project_id)

# 🔹 Load summaries.json
with open("summaries.json", "r") as f:
    summaries = json.load(f)

# 🔹 Load follow_up_log.json (crisis cases)
crisis_users = set()
if os.path.exists("follow_up_log.json"):
    with open("follow_up_log.json", "r") as f:
        crisis_log = json.load(f)
        crisis_users = {entry.get("name") for entry in crisis_log if entry.get("name")}

# 🔁 Update summaries with crisis flag and re-save to Firestore
for name, record in summaries.items():
    print(f"\n📤 Pushing: {name}")

    # If full intake not saved, attach empty or placeholder
    full_intake = record.get("full_intake", {
        "name": name,
        "concern": "Unknown",
        "timestamp": record.get("timestamp", datetime.now().isoformat())
    })

    # Add crisis_detected flag
    crisis_flag = name in crisis_users
    record["crisis_detected"] = crisis_flag
    record["full_intake"] = full_intake

    # ✅ Push to Firestore
    try:
        persistence.save_summary_with_data(record["summary"], record)
        print("✅ Summary and intake data saved to Firestore!")
    except Exception as e:
        print(f"❌ Error saving to Firestore: {e}")

# ✅ Safely overwrite updated summaries.json
try:
    with open("summaries.json", "w") as f:
        json.dump(summaries, f, indent=4)
    print("✅ summaries.json written successfully.")
except Exception as e:
    print(f"❌ Error saving to local JSON: {e}")
