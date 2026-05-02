# Neural Career Recommendation System (KIT AI Career Hub Pro)

An advanced, desktop-based AI Career Profile Generator and Resume Builder built in Python. This system uses a custom-trained **Machine Learning Engine** alongside **Google's Gemini Generative AI** to analyze a student's cognitive, technical, and interpersonal attributes, providing highly tailored career pathways and professional resumes.

## ✨ Features

- **Custom Machine Learning Model**: Uses a `RandomForestClassifier` trained on a rich synthetic dataset mimicking real-world psychometric distributions across 30 modern career paths.
- **Generative AI Insights**: Integrates Google Gemini API to analyze the ML results and dynamically generate a comprehensive paragraph highlighting "Required Skills", "Salary Ranges", and "Growth Trends".
- **Modern UI/UX**: Built entirely on `CustomTkinter` featuring a beautiful glassmorphism-inspired dark/light theme, interactive assessment sliders, and a 3-column Result grid.
- **Premium PDF Export**: Automatically converts the user's results into a highly stylized, multi-page presentation-grade PDF using `fpdf2` and `matplotlib` for dynamic visual charting of aptitude scores.
- **Local Fallbacks**: Continues to operate efficiently with fallback algorithms and static dummy data if the user does not possess a GEMINI API key.
- **SQLite Database**: Persistent user history and registration via local databases.
- **AI Resume Builder**: A premium new feature that takes your personal details, education, experience, and skills, then uses Gemini AI to automatically generate a powerful professional career objective, summary, and structured key strengths. Includes live preview and PDF export.
- **Project Summary Generator**: Includes `export_summary_pdf.py` to automatically generate a comprehensive multi-page summary of the app's architecture, technologies, sample resumes, career profiles, and code analysis.

## 🚀 Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/career-recommendation-system.git
   cd career-recommendation-system
   ```

2. **Install Dependencies**
   Install the required libraries listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
   .\.venv\Scripts\Activate.ps1  

3. **Configure API Keys (Optional but Recommended)**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

5. **Generate Project Summary Report**
   To generate a detailed technical PDF report showcasing the app's output features:
   ```bash
   python export_summary_pdf.py
   ```

## 🛠️ Technology Stack
- **Python 3.x**
- **Machine Learning**: `scikit-learn`, `numpy`
- **Generative AI**: `google-genai` SDK
- **GUI Framework**: `CustomTkinter`
- **Data Visualization**: `matplotlib`
- **PDF Generation**: `fpdf2`

## 📸 Screenshots
*(Add your screenshots here!)*

---
*Built for modern career guidance and advanced psychometric evaluation.*
