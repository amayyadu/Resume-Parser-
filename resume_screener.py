import os
import json
import time
import jsonschema
import pandas as pd
from jsonschema import validate, ValidationError
# Use the official Google GenAI SDK
from google import genai
from google.genai import types

# Initialize client (looks for GEMINI_API_KEY environment variable automatically)
client = genai.Client()

# ── Resume schema ──────────────────────────────────────────────────────────
RESUME_SCHEMA = {
    "type": "object",
    "properties": {
        "full_name":          {"type": "string"},
        "email":              {"type": ["string", "null"]},
        "years_experience":   {"type": "integer", "minimum": 0},
        "current_role":       {"type": "string"},
        "technical_skills":   {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "education_level":    {"type": "string", "enum": ["high_school", "bachelor", "master", "phd", "other"]},
        "previous_companies": {"type": "array", "items": {"type": "string"}},
        "languages":          {"type": "array", "items": {"type": "string"}}
    },
    "required": ["full_name", "years_experience", "current_role", "technical_skills", "education_level"]
}

# ── Job requirements for matching ─────────────────────────────────────────
JOB_REQUIREMENTS = {
    "title":               "Senior Data Scientist",
    "min_experience":       4,
    "required_skills":      ["Python", "SQL", "Machine Learning"],
    "preferred_skills":     ["PyTorch", "TensorFlow", "MLflow", "Spark"],
    "min_education":        "bachelor",
}

EDUCATION_RANK = {"high_school": 0, "bachelor": 1, "master": 2, "phd": 3, "other": 0}


def parse_resume(resume_text):
    """Extract structured candidate data from raw resume text using Gemini."""
    prompt = (
        f"Parse this resume and return JSON according to the schema provided.\n\n"
        f"Resume:\n{resume_text}"
    )
    
    try:
        # Request structured JSON matching our exact Pydantic/JSON Schema
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="Parse resumes into structured JSON.",
                response_mime_type="application/json",
                response_schema=RESUME_SCHEMA,
            ),
        )
        
        parsed = json.loads(response.text)
        
        # Double check schema integrity using jsonschema validation
        validate(instance=parsed, schema=RESUME_SCHEMA)
        return parsed
        
    except ValidationError as e:
        print(f"  ⚠️ Schema Validation error: {e.message}")
        return None
    except Exception as e:
        print(f"  ❌ API or parsing failure: {e}")
        return None


def score_candidate(candidate, requirements):
    """Score a parsed candidate against job requirements."""
    skills_lower = [s.lower() for s in candidate.get("technical_skills", [])]

    # ── Experience score (0–30 pts) ───────────────────────────────────────
    exp = candidate.get("years_experience", 0)
    exp_req = requirements["min_experience"]
    exp_score = min(30, int((exp / max(exp_req, 1)) * 30))

    # ── Required skills score (0–40 pts) ─────────────────────────────────
    req_skills = requirements["required_skills"]
    req_matches = sum(1 for s in req_skills if s.lower() in skills_lower)
    req_score = int((req_matches / len(req_skills)) * 40)

    # ── Preferred skills score (0–20 pts) ─────────────────────────────────
    pref_skills = requirements["preferred_skills"]
    pref_matches = sum(1 for s in pref_skills if s.lower() in skills_lower)
    pref_score = int((pref_matches / len(pref_skills)) * 20)

    # ── Education score (0–10 pts) ────────────────────────────────────────
    edu_level = candidate.get("education_level", "other")
    min_edu = requirements["min_education"]
    edu_score = 10 if EDUCATION_RANK.get(edu_level, 0) >= EDUCATION_RANK.get(min_edu, 0) else 0

    total = exp_score + req_score + pref_score + edu_score
    if total >= 80:    recommendation = "STRONG HIRE"
    elif total >= 60: recommendation = "PROCEED TO INTERVIEW"
    elif total >= 40: recommendation = "MAYBE — NEEDS REVIEW"
    else:              recommendation = "NOT SUITABLE"

    return {
        "experience_score" : exp_score,
        "required_skills"  : req_score,
        "preferred_skills" : pref_score,
        "education"        : edu_score,
        "total"            : total,
        "recommendation"   : recommendation,
        "matched_required" : [s for s in req_skills  if s.lower() in skills_lower],
        "matched_preferred": [s for s in pref_skills if s.lower() in skills_lower],
    }


# ── Sample resumes ─────────────────────────────────────────────────────────
RESUMES = [
    """
    Meera Iyer | meera.iyer@email.com
    Senior Data Scientist at FinEdge Analytics — 6 years total experience.
    M.Sc. Computer Science, IIT Bombay.
    Skills: Python, SQL, TensorFlow, PyTorch, MLflow, Spark, scikit-learn, Tableau.
    Languages: English, Hindi, Tamil.
    Previous: Infosys (2 years), Wipro (1.5 years).
    """,
    """
    Arjun Sharma | arjun.s@mail.com
    Junior Developer, 1.5 years experience.
    B.E. IT, VIT Vellore.
    Skills: HTML, CSS, JavaScript, React.
    Previous company: WebCraft Solutions.
    Languages: English, Telugu.
    """,
    """
    Dr. Sunita Rao
    Lead ML Engineer at DeepTech Labs — 9 years experience.
    Ph.D. in Machine Learning, IISc Bangalore.
    Skills: Python, SQL, PyTorch, TensorFlow, Spark, MLflow, Kubernetes, R, Scala.
    Former researcher at Microsoft Research and Google Brain.
    Languages: English, Kannada.
    """
]

# ── Run the full pipeline ──────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        print("Please export your key first: export GEMINI_API_KEY='your_key'")
        exit(1)

    print(f"JOB: {JOB_REQUIREMENTS['title']}")
    print(f"Required skills: {JOB_REQUIREMENTS['required_skills']}")
    print("=" * 65)

    for i, resume in enumerate(RESUMES, 1):
        print(f"\n🔍 Candidate {i}")
        candidate = parse_resume(resume)
        if candidate is None:
            print("  ❌ Resume parsing failed")
            continue

        scores = score_candidate(candidate, JOB_REQUIREMENTS)

        rec_icon = {"STRONG HIRE": "🟢", "PROCEED TO INTERVIEW": "🔵",
                    "MAYBE — NEEDS REVIEW": "🟡", "NOT SUITABLE": "🔴"}

        print(f"  Name       : {candidate['full_name']}")
        print(f"  Experience : {candidate['years_experience']} years")
        print(f"  Education  : {candidate['education_level']}")
        print(f"  Skills     : {', '.join(candidate['technical_skills'][:5])}...")
        print(f"  Score      : {scores['total']}/100  "
              f"(exp:{scores['experience_score']} req:{scores['required_skills']} "
              f"pref:{scores['preferred_skills']} edu:{scores['education']})")
        print(f"  Decision   : {rec_icon.get(scores['recommendation'], '❓')} {scores['recommendation']}")
        print(f"  Required ✓ : {scores['matched_required']}")
        print(f"  Preferred ✓: {scores['matched_preferred']}")
        time.sleep(0.5)
