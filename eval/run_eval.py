"""Mock-mode evaluation of the crisis check in CompassionateConnect AI.

Runs each synthetic intake form through the repo's real
IntakeQuestionnaireAgent.process_form_submission, with the Gemini and
Firestore SDKs replaced by inert stubs. No network, no keys, no cost.
Side-effect files (summaries.json, follow_up_log.json) go to a temp dir.

    python eval/run_eval.py          # prints a summary, writes eval/results.{md,json}

Labels in cases.jsonl are the author's own judgement on synthetic phrases.
They have NOT been reviewed by a clinician. Positive = "should be routed to a
human for urgent review". Uncertain answers are labelled positive on purpose.
"""
import ast
import contextlib
import inspect
import io
import json
import os
import re
import sys
import tempfile
import types
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent


def install_stubs():
    """Replace google.generativeai / google.cloud.firestore with inert stubs."""
    genai = types.ModuleType("google.generativeai")
    genai.configure = lambda **kw: None

    class _Model:
        def __init__(self, *a, **k): pass
        def generate_content(self, *a, **k):
            raise RuntimeError("LLM disabled in mock mode")
    genai.GenerativeModel = _Model

    firestore = types.ModuleType("google.cloud.firestore")

    class _Col:
        def add(self, *a, **k): return None
    class _Client:
        def __init__(self, *a, **k): pass
        def collection(self, *a, **k): return _Col()
    firestore.Client = _Client

    google = types.ModuleType("google")
    cloud = types.ModuleType("google.cloud")
    google.generativeai, google.cloud, cloud.firestore = genai, cloud, firestore
    sys.modules.update({
        "google": google, "google.generativeai": genai,
        "google.cloud": cloud, "google.cloud.firestore": firestore,
    })
    os.environ["GENAI_API_KEY"] = "mock"


def load_agent_class():
    install_stubs()
    sys.path.insert(0, str(ROOT))
    import intake_agent
    return intake_agent


def crisis_terms(module):
    """Read the keyword list out of the real detect_crisis source, so reporting
    of *which* term matched stays in sync with the code under test."""
    src = inspect.getsource(module.IntakeQuestionnaireAgent.detect_crisis)
    m = re.search(r"crisis_terms\s*=\s*(\[.*?\])", src, re.S)
    return ast.literal_eval(m.group(1))


def run_current(module, form, terms):
    """Run the real web-path intake step. Returns (flagged, matched_terms)."""
    with contextlib.redirect_stdout(io.StringIO()):  # repo code prints emoji; keep consoles happy
        agent = module.IntakeQuestionnaireAgent("mock-project")
        result = agent.process_form_submission(form)
    answer = str(form.get("crisis_check", "")).lower()
    matched = [t for t in terms if t in answer]
    # Guard: my term parsing must agree with the real detector.
    assert bool(matched) == result["crisis_flagged"], (form, matched, result)
    return result["crisis_flagged"], matched


def make_form(case):
    return {
        "name": "Test Person", "age": 30, "phone": "555-0100",
        "emergency_contact": "Test Contact", "current_mood": 5,
        "sleep_pattern": "Fair",
        "main_concern": case["main_concern"],
        "crisis_check": case["crisis_check"],
    }


def rate(n, d):
    return None if d == 0 else round(n / d, 3)


def main():
    module = load_agent_class()
    terms = crisis_terms(module)
    cases = [json.loads(l) for l in (HERE / "cases.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

    rows = []
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)  # keep summaries.json / follow_up_log.json out of the repo
        try:
            for c in cases:
                flagged, matched = run_current(module, make_form(c), terms)
                rows.append({**c, "flagged": flagged, "matched": matched})
        finally:
            os.chdir(cwd)

    tp = [r for r in rows if r["needs_review"] and r["flagged"]]
    fn = [r for r in rows if r["needs_review"] and not r["flagged"]]
    fp = [r for r in rows if not r["needs_review"] and r["flagged"]]
    tn = [r for r in rows if not r["needs_review"] and not r["flagged"]]
    # "Accidental" = matched only the letter y inside another word. A bare "Y" answer is a legitimate match.
    def only_y_in_word(r):
        return set(r["matched"]) == {"y"} and r["crisis_check"].strip().lower() != "y"
    accidental_tp = [r for r in tp if only_y_in_word(r)]
    accidental_fp = [r for r in fp if only_y_in_word(r)]
    pos_total = len(tp) + len(fn)
    ambiguous = [r for r in rows if r["category"] == "ambiguous"]
    free_text = [r for r in rows if r["category"] == "free_text_only"]
    tp_wo_amb = [r for r in tp if r["category"] != "ambiguous"]
    pos_wo_amb = pos_total - len(ambiguous)
    pos_screened_field = pos_total - len(free_text)

    by_cat = defaultdict(lambda: {"n": 0, "correct": 0})
    for r in rows:
        by_cat[r["category"]]["n"] += 1
        by_cat[r["category"]]["correct"] += int(r["needs_review"] == r["flagged"])

    summary = {
        "detector": "current (IntakeQuestionnaireAgent.process_form_submission)",
        "cases": len(rows), "positives": len(tp) + len(fn), "negatives": len(fp) + len(tn),
        "tp": len(tp), "fn": len(fn), "fp": len(fp), "tn": len(tn),
        "recall": rate(len(tp), len(tp) + len(fn)),
        "precision": rate(len(tp), len(tp) + len(fp)),
        "false_positive_rate": rate(len(fp), len(fp) + len(tn)),
        "flagged_only_via_y_inside_a_word": len(accidental_tp),
        "false_alarms_only_via_y_inside_a_word": len(accidental_fp),
        "recall_excluding_accidental_matches": rate(len(tp) - len(accidental_tp), pos_total),
        "recall_excluding_ambiguous_cases": rate(len(tp_wo_amb), pos_wo_amb),
        "recall_on_screened_field_only": rate(len(tp), pos_screened_field),
        "keyword_list": terms,
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "cases": rows}, indent=2, ensure_ascii=False), encoding="utf-8")

    def show(r):
        m = ", ".join(f"`{t}`" for t in r["matched"]) or "none"
        return f"| {r['id']} | {r['category']} | {r['crisis_check']!r} | {r['main_concern']!r} | {m} |"

    hdr = "| ID | Category | crisis_check answer | main_concern | Matched terms |\n|---|---|---|---|---|"
    md = [
        "# Crisis-check evaluation (mock mode)",
        "",
        "Generated by `eval/run_eval.py`. Deterministic; no network, keys or cloud services.",
        "",
        "**Read this first.** The 40 cases are synthetic phrases I wrote, and the labels are",
        "my own judgement. No clinician has reviewed them. This is a small development set",
        "used to expose gaps in the current detector, not a validation study, and the",
        "numbers say nothing about real-world performance.",
        "",
        "**Positive** means the form should be routed to a human for urgent review;",
        "uncertain or declined answers are labelled positive on purpose (fail safe).",
        "The detector under test is the real web-path code in `intake_agent.py`.",
        "",
        "## Headline",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Cases (positive / negative) | {summary['cases']} ({summary['positives']} / {summary['negatives']}) |",
        f"| **Recall** (risk cases flagged) | **{len(tp)}/{len(tp)+len(fn)} = {summary['recall']}** |",
        f"| Precision | {len(tp)}/{len(tp)+len(fp)} = {summary['precision']} |",
        f"| False-positive rate | {len(fp)}/{len(fp)+len(tn)} = {summary['false_positive_rate']} |",
        f"| Flagged risk cases that matched only via the letter `y` inside another word | {len(accidental_tp)} of {len(tp)} |",
        f"| False alarms caused only by the letter `y` inside another word | {len(accidental_fp)} of {len(fp)} |",
        "",
        "### Sensitivity (how much the labelling choices matter)",
        "",
        "| Variant | Recall |",
        "|---|---|",
        f"| Excluding accidental `y` matches from the true positives | {len(tp)-len(accidental_tp)}/{pos_total} = {summary['recall_excluding_accidental_matches']} |",
        f"| Excluding the {len(ambiguous)} ambiguous cases (uncertain/declined answers) | {len(tp_wo_amb)}/{pos_wo_amb} = {summary['recall_excluding_ambiguous_cases']} |",
        f"| Only the field the detector screens (drops the {len(free_text)} free-text-only cases) | {len(tp)}/{pos_screened_field} = {summary['recall_on_screened_field_only']} |",
        "",
        "Recall is the number that matters most here: a missed risk case is the costly error.",
        "",
        "## Accuracy by category",
        "",
        "| Category | Correct / Total |",
        "|---|---|",
    ] + [f"| {k} | {v['correct']}/{v['n']} |" for k, v in sorted(by_cat.items())] + [
        "",
        f"## Missed risk cases (false negatives): {len(fn)}",
        "",
        hdr,
    ] + [show(r) for r in fn] + [
        "",
        f"## Flagged, but only because the letter `y` appears inside another word: {len(accidental_tp)}",
        "",
        hdr,
    ] + [show(r) for r in accidental_tp] + [
        "",
        f"## False alarms (false positives): {len(fp)}",
        "",
        hdr,
    ] + [show(r) for r in fp] + [
        "",
        "## What this shows",
        "",
        "- Only the `crisis_check` field is screened, so risk language in `main_concern` is never seen.",
        "- Terms are matched as substrings, so short terms such as `y` and `die` fire inside ordinary words.",
        "- Misspellings, non-English answers and indirectly worded risk are missed.",
        "- False alarms are the safer error, but a detector that flags many clear \"no\" answers",
        "  trains staff to ignore it, and it still fails on the cases that matter.",
        "",
        "## Limits of this evaluation",
        "",
        "- Synthetic, author-labelled, single-language, 40 cases; not clinician-reviewed.",
        "- Tests only the rule-based check. LLM output (crisis reply, summaries, insights) is not evaluated in mock mode.",
        "- Not evidence about any real patient population.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python eval/run_eval.py   # Python 3.9+; standard library only",
        "```",
        "",
    ]
    (HERE / "results.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps({k: v for k, v in summary.items() if k != "keyword_list"}, indent=2))
    print("wrote eval/results.md and eval/results.json")


if __name__ == "__main__":
    main()
