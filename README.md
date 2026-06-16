# 🧠 CompassionateConnect AI
**Empathetic Multi-Agent Mental Health Onboarding System using Gemini + Firestore**

*Built for the Google Cloud Multi-Agent Hackathon · June 2025*

## 🚨 The Problem
Mental health clinics are overwhelmed with intake admin work. Patients feel unseen, crisis moments go unnoticed, and clinicians don't get usable summaries before sessions. And they have to do so many tasks that distract them and burden them from giving their full to the patient.

## 💡 My Solution
CompassionateConnect AI is a multi-agent system that reimagines mental health onboarding using conversational AI.

It:
- Uses Gemini to clarify patient responses in real time
- Detects crisis phrases and initiates a follow-up protocol
- Summarizes intake sessions into therapist-friendly briefs
- Suggests potential therapy areas using non-diagnostic AI
- Stores everything in Firestore + local JSON

## 🧠 Architecture

### 🤖 Agent Overview
| Agent | Role |
|-------|------|
| OnboardingCoordinatorAgent | Orchestrates the full flow from intake to summary |
| IntakeQuestionnaireAgent | Asks, validates, and clarifies patient responses (Gemini-powered) |
| CrisisResponseAgent | Detects crisis indicators and logs high-priority cases |
| SummaryGeneratorAgent | Converts responses into natural language summaries |
| InsightAgent | Suggests possible therapy directions for therapists |
| DataPersistenceAgent | Saves to Firestore and local JSON for dashboard use |

## 🧪 Try It Out (Local CLI Demo)
```bash
git clone https://github.com/Hereforlolz/compassionateconnect.git
cd compassionateconnect
pip install -r requirements.txt

# Start the intake flow:
uvicorn api_main:app --reload

# Open the link in the web browser and enter data to see the backend cli and the AI insights to show up after clicking submit :
http://127.0.0.1:8000

# View the therapist dashboard:
python therapist_dashboard.py
```

You'll experience a fully guided, AI-powered intake simulation — with clarifications, summaries, and ethical insights.

## 🧰 Tech Stack
- 🧠 Gemini 1.5 Flash (via `google.generativeai`)
- 🔐 Firestore for real-time clinician-side storage
- 🐍 Python multi-agent architecture
- 🗃️ JSON for local offline demo + backups
- 💬 Command-line interface

## 📺 Demo Video
https://www.youtube.com/watch?v=exSmOzVHLIg&ab_channel=SreenidhiVedartham%28Needhi%29

## 🧾 Therapist Dashboard
The dashboard:
- Displays client summaries
- Shows ethically filtered Gemini-generated insights
- Flags any crisis-detected users for immediate follow-up
- Simulates a therapist dashboard to help summarize quickly

## 🧠 Ethical AI Design
- ❌ No diagnoses — only therapist-facing suggestions
- 💬 Clear disclaimers in every AI insight
- 🛡️ Simulated patient data only
- 👥 Built to augment, not replace, human clinicians

## 📘 Notion Documentation
👉 [View full Notion project book](https://www.notion.so/CompassionateConnect-AI-20eb2f6a587d809194b4dfadbf393ebb?source=copy_link)

## 🚀 Commercial & Partnership Opportunities

This system demonstrates production-ready multi-agent orchestration in healthcare AI. The architecture scales to enterprise environments and addresses real market needs in the $4B+ mental health technology sector.

### 🌐 Enterprise Integration Capabilities
- **Scalable multi-agent orchestration** for healthcare systems
- **HIPAA-compliant architecture** ready for production deployment
- **Crisis intervention protocols** with real-time alerting
- **Customizable therapy insight generation** for different clinical approaches

---

## 🧭 Project Files (Flat Structure)
```
compassionateconnect/
├── Templates/
├── intake_agent.py
├── crisis_response_agent.py
├── summary_generator_agent.py
├── insight_agent.py
├── data_persistence_agent.py
├── onboarding_coordinator_agent.py
├── therapist_dashboard.py
├── summaries.json
├── follow_up_log.json
├── requirements.txt
├── api_main.py
├── README.md
└── LICENSE
```

## 🧠 For Judges
✅ Multi-Agent GenAI system
✅ Gemini 1.5 Flash + Firestore integration
✅ Crisis-aware, ethically aligned
✅ Dashboard for therapists
✅ Notion doc + demo included

## 📜 License
This project is licensed under the MIT License.

---

*"The best AI systems are the ones that make human connection more possible, not less."*
