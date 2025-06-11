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
        # Save to Firestore
        client_name = patient_data.get("name", "Unnamed Client")
        timestamp = patient_data.get("crisis_timestamp") or patient_data.get("timestamp") or datetime.now().isoformat()

        summary_record = {
            "summary": summary_text,
            "timestamp": timestamp,
            "crisis_detected": patient_data.get("crisis_detected", False),
            "full_intake": patient_data
         }
         #save to firestore
        try:
            self.db.collection("summaries_with_data").document(client_name).set(summary_record)
            print("✅ Summary and intake data saved to Firestore!")
        except Exception as e:
            print(f"❌ Error saving summary with data: {e}")

    # 🔹 Save to local summaries.json (as a dict)
        try:
            file_path = "summaries.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    local_data = json.load(f)
            else:
                local_data = {}

            local_data[client_name] = summary_record

            with open(file_path, "w") as f:
                json.dump(local_data, f, indent=2)

            print("🗃️ Summary also saved locally to summaries.json")
        except Exception as e:
            print(f"❌ Error saving to local JSON: {e}")