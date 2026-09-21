# CompassionateConnect AI
**A multi-agent prototype for mental-health clinic intake**

*Built for the Google Cloud Multi-Agent Hackathon · June 2025*

> **Status: archived hackathon demo. Not a clinical system.**
> All data in this repo is synthetic. It has never been used with real
> patients, is not HIPAA-compliant, has not been clinically validated, and its
> crisis check is a keyword match, not a risk assessment. Anything crisis-related
> or sensitive must be reviewed by a human clinician.
> The original cloud resources (Firestore project, hosted demo) have been shut down.

**Read first:** [Case study](docs/case-study.md) · [Architecture diagram](docs/architecture.svg)

---

## The Problem

Mental health clinics carry heavy intake admin. Crisis signals can be missed,
and clinicians often start a session without a usable summary. The hackathon
question: can a set of small, specialised agents handle intake so clinicians
spend their time on patients?

---

## What Is Actually Implemented

There are two entry points, and they do **not** run the same agents.

| Component | What it does | LLM? | Runs in |
|-----------|--------------|------|---------|
| `IntakeQuestionnaireAgent` | Asks 8 questions, validates answers with rules, checks the `crisis_check` answer against a keyword list | Gemini only writes clarification text | CLI + web |
| `CrisisResponseAgent` | Writes a short supportive message pointing to 988; falls back to fixed 911 text | Yes | CLI + web |
| `InsightAgent` | Suggests possible therapy directions with a "not a diagnosis" disclaimer | Yes | CLI + web + dashboard |
| `SummaryGeneratorAgent` | Turns intake data into a clinician-facing brief | Yes | CLI only |
| `DataPersistenceAgent` | Writes to Firestore and `summaries.json` | No | CLI only |
| `OnboardingCoordinatorAgent` | Sequences the agents above | No | CLI only |

The web path (`api_main.py`) builds its summary from a plain string template and
skips the coordinator, summary and persistence agents.

`coordinator_agent.py` and `followup_agent.py` are unused early experiments
(Vertex AI, `chat-bison`).

**Simulated or not implemented:** staff alerting (a `print` statement), sending
follow-up messages (a template is logged, nothing is sent), and crisis flags in
the therapist dashboard (it does not display them).

See the [case study](docs/case-study.md) for known gaps and what a real
version would require.

---

## Human-Review Design

- Insights are framed as suggestions for a therapist, never diagnoses, and carry a disclaimer.
- In the CLI flow the patient confirms or edits their answers before anything is saved.
- Crisis-related output is intended to go to a clinician. **No queue, alerting, or audit trail exists in this code.**

---

## Tech Stack

- Gemini via `google.generativeai` (code targets `gemini-1.5-flash`; that model name may need updating)
- Firestore (optional; failures are caught and the app continues)
- FastAPI + Uvicorn + Jinja2
- Local JSON files

---

## Running It Locally

Not currently turnkey. Known blockers:

- `intake_agent.py` requires `GENAI_API_KEY`; `summary_generator_agent.py` requires `GOOGLE_API_KEY`; `insight_agent.py` has a hardcoded `"YOUR_KEY"` placeholder to replace.
- Model names may need updating, and a Gemini key is required for any LLM output.
- Firestore is not needed to start the web app, but writes fail with a logged warning.
- The web path appends one JSON object per line to `summaries.json`, while the dashboard expects a single JSON object keyed by name.
- There are no automated tests; `test*.py` and `demo_script.py` are manual scripts.

```bash
git clone https://github.com/Hereforlolz/Compassionate-connect.git
cd Compassionate-connect
pip install -r requirements.txt
export GENAI_API_KEY=...  GOOGLE_API_KEY=...   # your own keys
uvicorn api_main:app --reload                   # http://127.0.0.1:8000
python therapist_dashboard.py                   # reads summaries.json
```

---

## What I'd Do Differently

**Agent boundaries were too loose.** The crisis and summary steps shared state,
which created ordering dependencies. A production design would enforce input and
output contracts and route through a message bus instead of direct calls.

**Prompt tuning was underinvested.** Clarifications sometimes read as clinical
rather than conversational.

**No eval harness.** I tracked whether the system ran, not whether its output
was good. Crisis detection and summary quality would need structured evaluation
before any clinical use.

---

## Files

```
├── api_main.py                      web entry point (FastAPI)
├── main.py, demo_script.py          CLI entry points
├── onboarding_coordinator_agent.py  CLI orchestration
├── intake_agent.py                  questions, validation, crisis keywords
├── crisis_response_agent.py
├── summary_generator_agent.py
├── insight_agent.py
├── data_persistence_agent.py
├── therapist_dashboard.py           CLI dashboard over summaries.json
├── templates/                       intake form and thank-you page
├── docs/                            case study and architecture diagram
├── summaries.json, follow_up_log.json   synthetic sample data
└── coordinator_agent.py, followup_agent.py   unused experiments
```

**License:** none specified yet (the earlier README said MIT, but no LICENSE file was ever added).

Follow-on prototype: [Therapist-Dashboard-AWS](https://github.com/Hereforlolz/Therapist-Dashboard-AWS).
