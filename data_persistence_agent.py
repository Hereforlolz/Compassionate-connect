# data_persistence_agent.py
from google.cloud import firestore

class DataPersistenceAgent:
    def __init__(self, project_id):
        self.db = firestore.Client(project=project_id)

    def save_data(self, data):
        try:
            doc_ref = self.db.collection("intake_forms").add(data)
            print("✅ Data saved to Firestore!")
        except Exception as e:
            print(f"❌ Error saving to Firestore: {e}")
