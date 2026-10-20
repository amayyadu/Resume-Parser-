# AI-Powered Resume Screening App

## Files
- `app.py`: Streamlit application
- `requirements.txt`: dependencies

## Run locally
1. Install Python 3.10+.
2. In this folder run: `pip install -r requirements.txt`
3. Set the environment variable `GEMINI_API_KEY` or use Streamlit secrets.
4. Create `.streamlit/secrets.toml` with:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Run: `streamlit run app.py`

Do not commit `.streamlit/secrets.toml` or your API key to GitHub.

## Deploy
Push `app.py` and `requirements.txt` to a GitHub repository. On Streamlit Community Cloud, create an app from that repository and entrypoint `app.py`. In Advanced settings / Secrets, add:
`GEMINI_API_KEY = "your-key-here"`

This app accepts text-based PDF, DOCX, and TXT files. Scanned PDFs may require OCR, which is not included.
