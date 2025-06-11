from google.cloud import firestore
from datetime import datetime
import json
import os

class DataPersistenceAgent:
    def __init__(self, project_id):
        self.db = firestore.Client(project=project_id)

    def save_data(self, data):
        try:
            self.db.collection("intake_forms").add(data)
            print("✅ Data saved to Firestore!")
        except Exception as e:
            print(f"❌ Error saving to Firestore: {e}")

    def save_summary_with_data(self, summary_text, patient_data):
        # ✅ Save to Firestore
        try:
            entry = {
                "summary": summary_text,
                "patient_data": patient_data,
                "timestamp": patient_data.get("crisis_timestamp") or
                             patient_data.get("timestamp") or
                             datetime.now().isoformat()
            }
            self.db.collection("summaries_with_data").add(entry)
            print("✅ Summary and intake data saved to Firestore!")
        except Exception as e:
            print(f"❌ Error saving summary with data to Firestore: {e}")

        # ✅ Also save to local JSON
        try:
            summary_entry = {
                "summary": summary_text,
                "timestamp": datetime.now().isoformat()
            }

            file_path = "summaries.json"

            # Use a separate variable to avoid overwriting input `patient_data`
            local_summaries = []
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    local_summaries = json.load(f)

            local_summaries.append(summary_entry)

            with open(file_path, "w") as f:
                json.dump(local_summaries, f, indent=2)

            print("🗃️ Summary also saved locally to summaries.json")
        except Exception as e:
            print(f"❌ Error saving summary to local JSON: {e}")

    def save_crisis_profile(self, patient_data):
        try:
            entry = {
                "name": patient_data.get("name"),
                "age": patient_data.get("age"),
                "main_concern": patient_data.get("main_concern"),
                "mood": patient_data.get("current_mood"),
                "timestamp": patient_data.get("crisis_timestamp", datetime.now().isoformat()),
                "crisis_flagged": True
            }
            self.db.collection("crisis_profiles").add(entry)
            print("🚨 Crisis profile saved to Firestore.")
        except Exception as e:
            print(f"❌ Error saving crisis profile: {e}")
