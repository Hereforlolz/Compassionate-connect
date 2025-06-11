# followup_agent.py

from datetime import datetime, timedelta
from google.cloud import firestore
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
import json

class FollowUpAgent:
    def __init__(self, project_id: str, location: str = "us-central1"):
        vertexai.init(project=project_id, location=location)
        self.chat_model = ChatModel.from_pretrained("chat-bison")
        self.db = firestore.Client(project=project_id)

    def generate_followup_message(self, user_name: str):
        prompt = f"Write a kind and empathetic message to check in on someone named {user_name} who reported a mental health crisis yesterday. Be gentle and supportive, and offer to help schedule an appointment."

        chat = self.chat_model.start_chat()
        response = chat.send_message(prompt)
        return response.text.strip()

    def fetch_recent_crisis_users(self):
        crisis_ref = self.db.collection("crisis_flags")
        yesterday = datetime.utcnow() - timedelta(days=1)

        query = crisis_ref.where("timestamp", ">=", yesterday)
        docs = query.stream()

        flagged_users = []
        for doc in docs:
            data = doc.to_dict()
            flagged_users.append(data)

        return flagged_users

    def send_followups(self):
        users = self.fetch_recent_crisis_users()
        followups = []

        for user in users:
            name = user.get("name", "there")
            message = self.generate_followup_message(name)

            followup_entry = {
                "user_id": user.get("user_id", "unknown"),
                "name": name,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            }

            followups.append(followup_entry)

            # Optional: Log to Firestore
            self.db.collection("followups").add(followup_entry)

        # Also write to JSON
        with open("followup_logs.json", "w") as f:
            json.dump(followups, f, indent=2)

        return followups
if __name__ == "__main__":
    PROJECT_ID = "compassionate-connect-ai"

    agent = FollowUpAgent(project_id=PROJECT_ID)
    results = agent.send_followups()

    for r in results:
        print(f"\nTo: {r['name']}\nMessage: {r['message']}\n")