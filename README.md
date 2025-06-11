README.md
# 🧠 CompassionateConnect AI
*Empathetic Multi-Agent Mental Health Onboarding System using Gemini + Firestore*

## 🚨 Problem

Traditional patient intake in mental health clinics is often:
- Rigid, confusing, and impersonal
- Not designed for emotional nuance or clarification
- Lacking crisis detection or follow-up mechanisms
- A burden on both patients and clinical staff

---

## 💡 Solution

**CompassionateConnect AI** is a multi-agent system that reimagines mental health onboarding using conversational AI. 

It simulates a human-like intake assistant that:
- Asks questions and clarifies them using AI (Gemini)
- Detects crisis phrases and redirects to emergency resources
- Logs summaries for therapist handoff
- Provides AI-powered **non-diagnostic** therapy suggestions
- Stores data securely in Firestore and locally in JSON

---

## 🤖 Multi-Agent Architecture

```mermaid
flowchart TD
    A[🧍 User] --> B(OnboardingCoordinatorAgent)
    
    subgraph Intake Flow
        B --> C[IntakeQuestionnaireAgent]
        C --> D{Response Type}
        D -->|Clarification| C
        D -->|Valid Answer| E[Store in patient_data]
        D -->|Crisis Detected| F[CrisisResponseAgent]
    end

    subgraph Post-Intake
        E --> G[SummaryGeneratorAgent]
        G --> H[InsightAgent]
        H --> I[DataPersistenceAgent]
    end

    F --> I
    F --> J[Follow-up Log (Firestore + JSON)]

    I --> K[Firestore: summaries_with_data]
    I --> L[Firestore: crisis_profiles]
    I --> M[Local JSON: summaries.json]

---

## 🔍 Agents Overview

| Agent                     | Role                                                                    |
|---------------------------|-------------------------------------------------------------------------|
| `OnboardingCoordinatorAgent` | Orchestrates the entire intake workflow                              |
| `IntakeQuestionnaireAgent`  | Asks, validates, and clarifies patient responses (via Gemini)         |
| `CrisisResponseAgent`       | Detects and responds to crisis-related language                       |
| `SummaryGeneratorAgent`     | Converts data into summaries for therapist use                        |
| `InsightAgent`              | Suggests non-diagnostic therapy paths based on the summary            |
| `DataPersistenceAgent`      | Stores patient data (Firestore + local JSON)                          |


---

## 🧪 Try It Out (Local CLI Demo)

```bash
git clone https://github.com/yourusername/compassionateconnect-ai.git
cd compassionateconnect-ai
pip install -r requirements.txt

python demo_script.py



    You'll experience a fully guided, AI-powered intake simulation.

🧰 Tech Stack

    🧠 Google Gemini 1.5 Flash (google.generativeai)

    🔐 Firestore (for real-time secure storage)

    🐍 Python (multi-agent architecture)

    🗃️ JSON files for local backup + testing

    💬 Command-line simulation (for demo)

📺 Demo Video

👉 Watch demo (2:45)
🧾 Therapist Dashboard

python therapist_dashboard.py

This will:

    Display all summaries

    Show ethical insights for therapists

    Include crisis-flagged profiles for review

🧠 Ethical AI Design

    ❌ No diagnoses — only suggestions

    💬 Clear disclaimers provided to users + clinicians

    🛡️ Simulated patient data only

    👥 System designed to augment, not replace, human care

🌐 Notion Documentation

Full project breakdown:
👉 View Notion project book
📁 Folder Structure

├── agents/
│   ├── intake_agent.py
│   ├── crisis_response_agent.py
│   ├── summary_generator_agent.py
│   ├── insight_agent.py
│   └── data_persistence_agent.py
├── onboarding_coordinator_agent.py
├── demo_script.py
├── therapist_dashboard.py
├── summaries.json
├── follow_up_log.json
├── requirements.txt
├── README.md
└── LICENSE

🧠 For Judges

✅ Multi-Agent AI system
✅ Uses Google Cloud (Gemini + Firestore)
✅ Crisis intervention flow
✅ Ethical guardrails
✅ Notion doc + demo video included
📜 License

This project is licensed under the MIT License.
