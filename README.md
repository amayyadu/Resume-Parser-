# AI-Powered Resume Screening System

A Python, Streamlit, and Google Gemini-based application that extracts resume details, matches candidates against job requirements, and generates explainable screening scores.

## Key Features
- Upload multiple PDF, DOCX, and TXT resumes.
- Extract candidate details and technical skills using Gemini.
- Calculate category-wise scores and recommendations.
- View matched skills and download results as CSV.

## Grading Criteria (100 Points)

| Category | Maximum | How Points Are Awarded |
|---|---:|---|
| Professional Experience | 30 | Based on years of experience compared with the minimum required. |
| Required Skills | 40 | Points proportional to the number of required skills matched. |
| Preferred Skills | 20 | Points proportional to the number of preferred skills matched. |
| Education | 10 | Awarded if the candidate meets the minimum education requirement. |

### Which Skills Earn Points?

**Default required skills — 40 points**
- Python
- SQL
- Machine Learning

Each matched skill earns approximately 13.33 points (40 ÷ 3), with the category score rounded down to an integer.

**Default preferred skills — 20 points**
- PyTorch
- TensorFlow
- MLflow
- Apache Spark

Each matched skill earns 5 points (20 ÷ 4).

These are the application's default criteria for its Senior Data Scientist profile. Change them in the sidebar to match the actual job description. Skills outside these lists do not earn separate skill-match points unless added to the criteria.

The app uses normalized skill matching and selected aliases; it does not fully evaluate proficiency or infer every semantically equivalent skill.

### Other Scoring Rules

- **Experience:** `min(30, int(candidate_years / required_years × 30))`. If minimum required experience is zero, the app awards 30 points.
- **Education:** 10 points if the candidate's education rank meets the selected minimum; otherwise, 0. The ranking is High School (0), Bachelor's (1), Master's (2), PhD (3), Other (0).
- **Total:** Sum of all four category scores.

## Recommendation Thresholds

| Score | Recommendation |
|---:|---|
| 80–100 | STRONG MATCH - REVIEW |
| 60–79 | INTERVIEW REVIEW |
| 40–59 | MANUAL REVIEW |
| 0–39 | LOW MATCH - REVIEW |

These labels reflect configured criteria, not guaranteed job performance.

## Tech Stack
Python · Streamlit · Google Gemini API · Pandas · JSON Schema · pypdf · python-docx

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Configure your Gemini API key in `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-api-key"
```

Never commit your API key to GitHub.

## Deployment
Deploy the GitHub repository through [Streamlit Community Cloud](https://share.streamlit.io/) and add `GEMINI_API_KEY` in the app's Secrets settings.

## Limitations & Responsible Use
Scanned PDFs without extractable text are not supported. Resume extraction and skill matching can be inaccurate; verify results manually. Project quality, certifications, and soft skills do not receive separate points in the current scoring formula. Protect candidate data and never use the score as the sole basis for hiring decisions.
