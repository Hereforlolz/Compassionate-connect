# api_main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from intake_agent import IntakeQuestionnaireAgent
from crisis_response_agent import CrisisResponseAgent
from insight_agent import InsightAgent

from google.cloud import firestore
import os

# === CONFIG ===
PROJECT_ID = "compassionate-connect-ai"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

# === INIT FASTAPI ===
app = FastAPI(
    title="CompassionateConnect AI",
    description="Multi-agent mental health onboarding system",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

# === INIT AGENTS ===
intake_agent = IntakeQuestionnaireAgent(PROJECT_ID)
crisis_agent = CrisisResponseAgent(PROJECT_ID)
insight_agent = InsightAgent()

# === ROUTES ===

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("intake_form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    phone: str = Form(...),
    emergency_contact: str = Form(...),
    current_mood: int = Form(...),
    sleep_pattern: str = Form(...),
    main_concern: str = Form(...),
    crisis_check: str = Form(...)
):
    # === 1) Collect form ===
    form_data = {
        "name": name,
        "age": age,
        "phone": phone,
        "emergency_contact": emergency_contact,
        "current_mood": current_mood,
        "sleep_pattern": sleep_pattern,
        "main_concern": main_concern,
        "crisis_check": crisis_check
    }

    # === 2) Intake Agent: store, check crisis ===
    intake_result = intake_agent.process_form_submission(form_data)

    # === 3) If crisis, handle it ===
    if intake_result["crisis_flagged"]:
        crisis_agent.handle_crisis(form_data)

    # === 4) Insight Agent: generate suggestions ===
    insights = insight_agent.generate_insights(intake_result["summary"])

    # === 5) Return thank-you page ===
    return templates.TemplateResponse(
        "thank_you.html",
        {
            "request": request,
            "summary": intake_result["summary"],
            "crisis": intake_result["crisis_flagged"],
            "insights": insights
        }
    )

@app.get("/ping")
def ping():
    return {"message": "CompassionateConnect AI API is alive!"}
