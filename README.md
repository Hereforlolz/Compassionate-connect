# CompassionateConnect AI
**Multi-Agent Mental Health Intake System**

*Built for the Google Cloud Multi-Agent Hackathon · 
June 2025 · Status: Archived / Demo Only*

---

## The Problem

Mental health clinics are overwhelmed with intake 
admin work. Patients feel unseen, crisis moments go 
unnoticed, and clinicians don't get usable summaries 
before sessions.

CompassionateConnect reimagines that intake process 
using a multi-agent conversational AI system — so 
clinicians spend less time on paperwork and more 
time with patients.

---

## What It Does

Six agents handle the full intake flow:

| Agent | Role |
|-------|------|
| OnboardingCoordinatorAgent | Orchestrates the full flow |
| IntakeQuestionnaireAgent | Asks, validates, clarifies patient responses in real time |
| CrisisResponseAgent | Detects crisis indicators, logs high-priority cases |
| SummaryGeneratorAgent | Converts responses into therapist-friendly briefs |
| InsightAgent | Suggests possible therapy directions (non-diagnostic) |
| DataPersistenceAgent | Saves to Firestore and local JSON |

Each agent operates independently with a defined 
input/output contract — the coordinator sequences 
them and handles exceptions.

---

## Ethical AI Design

This was a design constraint, not an afterthought:

- No diagnoses — AI surfaces directions for 
  therapists to evaluate, not conclusions
- Clear disclaimers embedded in every AI insight
- Simulated patient data only — no real PHI at 
  any stage
- Built to augment clinicians, not replace them

---

## Tech Stack

- Gemini 1.5 Flash (via `google.generativeai`)
- Firestore for real-time clinician-side storage
- FastAPI + Uvicorn
- Python multi-agent architecture
- Local JSON for offline demo and backup

---

## Try It Locally

```bash
git clone https://github.com/Hereforlolz/compassionateconnect.git
cd compassionateconnect
pip install -r requirements.txt

# Start the intake flow:
uvicorn api_main:app --reload
# Open: http://127.0.0.1:8000

# View therapist dashboard:
python therapist_dashboard.py
```

---

## What I'd Do Differently

**Agent boundaries were too loose.** The 
CrisisResponseAgent and SummaryGeneratorAgent shared 
state in ways that created ordering dependencies. 
In a production system I'd enforce stricter 
input/output contracts and add a message bus rather 
than direct agent-to-agent calls.

**Gemini prompt tuning was underinvested.** The 
IntakeAgent clarifications sometimes felt clinical 
rather than conversational — the prompt needed more 
iteration than the hackathon timeline allowed.

**No eval harness.** I tracked whether the system 
ran, not whether the outputs were actually good. 
A real deployment would need structured evaluation 
of summary quality and crisis detection accuracy 
before any clinical use.

---

## Project Files

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
├── api_main.py
├── requirements.txt
├── summaries.json
├── follow_up_log.json
└── README.md
```

*MIT License · Part of a broader exploration of 
AI systems for underserved healthcare contexts.*
