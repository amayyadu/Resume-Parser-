# AI Resume Screener & Ranking Pipeline

An automated recruitment tool that converts unstructured resume text into validated, schema-strict JSON arrays using LLMs, then runs a deterministic, weighted scoring algorithm to screen candidates.

## 🚀 Key Framework Features
* **Structured Parsing:** Uses `gemini-2.5-flash` with a strict `response_schema` to parse raw text into clean data profiles.
* **Schema Validation:** Leverages `jsonschema` to guarantee structural and data-type integrity before evaluation.
* **Weighted Evaluation Matrix:** Calculates matching metrics up to 100 points across Experience (30%), Core Skills (40%), Preferred Skills (20%), and Education (10%).

## ⚙️ Setup & Execution

1. **Clone the Repo & Install Requirements:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME
   pip install -r requirements.txt
