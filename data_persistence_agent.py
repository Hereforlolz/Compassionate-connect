# data_persistence_agent.py
import os
import json
from datetime import datetime
from google.cloud import firestore

class DataPersistenceAgent:
    def __init__(self, project_id):
        self.db = firestore.Client(project=project_id)

    def save_data(self, data):
        try:
            self.db.collection("intake_forms").add(data)
            print(" Data saved to Firestore!")
        except Exception as e:
            print(f" Error saving to Firestore: {e}")

    def save_summary_to_json(self, summary_text):
        log_path = "summaries.json"
        summary_entry = {
            "summary": summary_text,
            "timestamp": datetime.now().isoformat()
        }

        try:
            if os.path.exists(log_path):
                with open(log_path, "r") as f:
                    data = json.load(f)
            else:
                data = []

            data.append(summary_entry)

            with open(log_path, "w") as f:
                json.dump(data, f, indent=2)


        except Exception as e:
            print(f" Error saving summary to JSON: {e}")
