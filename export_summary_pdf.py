from fpdf import FPDF

SUMMARY = '''AI Career Recommendation Hub (desktop app)

Purpose:
Evaluate a user's skills via a 12-slider psychometric assessment and provide AI-driven career recommendations plus detailed career insights.

How the app works (step-by-step):
1. Launch the app: run `python main.py` to open the `AdvancedCareerApp` GUI.
2. Authenticate: user can sign in or register (local in-memory DB / persisted DB per README).
3. Dashboard: user navigates to the "Neural Assessment" screen from the sidebar.
4. Input: user adjusts 12 sliders corresponding to features (e.g., Mathematics, Communication, Creative Ability, Extroversion).
5. Start analysis: user clicks "Run ML Analysis Pipeline".
6. Preprocessing/UI: app shows a loading overlay and collects the 12 feature values.
7. ML inference: `MLPredictor.predict()` scales inputs with a saved `StandardScaler` and runs a trained `RandomForestClassifier` to get probabilities for career classes — returns top-3 recommendations with probabilities.
8. Generative insight: primary career label is passed to `get_career_insights()` which calls Gemini API if `GEMINI_API_KEY` is set, otherwise returns a local fallback.
9. Finalization: UI displays the recommended career(s), confidence, and generated insight; result is appended to user's history.
10. Export & history: user can view past results in "Results History" and export a stylized PDF summary using `fpdf2`.
11. Offline behavior: if Gemini API is unavailable, the system still runs using local fallback insights and the ML model.

Key files / components:
- `main.py`: GUI, user flow, slider inputs, orchestration of ML + AI pipeline, UI screens, history handling.
- `ml_engine.py`: synthetic dataset generation, training, `MLPredictor` that loads/trains model and provides `predict(features)`.
- `ai_service.py`: wraps Google Gemini calls and contains `generate_fallback_insights()`.
- `README.md`: setup, run instructions, and a features overview.
- `requirements.txt`: dependency list needed to run the app.

How to run (concise):
1. Create and activate your venv, install deps:
   pip install -r requirements.txt
2. (Optional) Add Gemini key to `.env`:
   GEMINI_API_KEY=your_key_here
3. Start the app:
   python main.py

Important dependencies (most relevant):
- customtkinter (GUI)
- numpy, scikit-learn (ML)
- google-genai (Gemini client)
- python-dotenv (env vars)
- fpdf2, matplotlib (PDF/visuals)

Quick suggestions:
- Persist users/history in a real local DB (SQLite).
- Add input validation and better error handling around model/scaler loading.
- Provide a small test dataset and a CLI test to validate ML + fallback path without launching GUI.
- Limit heavy dependency versions in `requirements.txt` for reproducible installs.
'''

def create_pdf(text, out_path='project_summary.pdf'):
   pdf = FPDF()
   pdf.set_auto_page_break(auto=True, margin=15)
   pdf.add_page()
   pdf.set_font('Arial', size=12)

   for paragraph in text.split('\n\n'):
      pdf.multi_cell(0, 8, paragraph)
      pdf.ln(2)

   pdf.output(out_path)
   print(f'Wrote PDF: {out_path}')

def sanitize_text(text: str) -> str:
   # Replace common unicode punctuation with ASCII equivalents
   replacements = {
      '\u2014': '-',  # em dash
      '\u2013': '-',  # en dash
      '\u2018': "'",  # left single quote
      '\u2019': "'",  # right single quote
      '\u201c': '"',  # left double quote
      '\u201d': '"',  # right double quote
      '\u2026': '...',  # ellipsis
   }
   for k, v in replacements.items():
      text = text.replace(k, v)
   return text


if __name__ == '__main__':
   create_pdf(sanitize_text(SUMMARY))
