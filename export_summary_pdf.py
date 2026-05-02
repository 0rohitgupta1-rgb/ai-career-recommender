from fpdf import FPDF


def sanitize(text: str) -> str:
    """Replace unicode chars with ASCII equivalents for fpdf Helvetica font."""
    replacements = {
        '\u2014': '-', '\u2013': '-',
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2026': '...', '\u2022': '*',
        '\u2726': '*', '\u2713': 'v',
        '\u2714': 'v', '\u2605': '*',
        '\u00a0': ' ', '&': '&',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')


class ReportPDF(FPDF):
    PRIMARY   = (31, 111, 235)    # blue
    SECONDARY = (46, 160, 67)     # green
    WARN      = (218, 54, 51)     # red
    PURPLE    = (137, 87, 229)    # purple
    LIGHT_BG  = (235, 244, 255)   # pale blue
    DARK_TEXT = (30, 30, 30)
    MID_TEXT  = (80, 80, 80)

    def colored_header(self, title: str, subtitle: str = '', color=None):
        c = color or self.PRIMARY
        self.set_fill_color(*c)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 18)
        self.cell(0, 14, sanitize(title), new_x='LMARGIN', new_y='NEXT', fill=True, align='C')
        if subtitle:
            darker = tuple(max(v - 30, 0) for v in c)
            self.set_font('Helvetica', '', 11)
            self.set_fill_color(*darker)
            self.cell(0, 8, sanitize(subtitle), new_x='LMARGIN', new_y='NEXT', fill=True, align='C')
        self.set_text_color(*self.DARK_TEXT)
        self.ln(5)

    def section_title(self, title: str, color=None):
        c = color or self.PRIMARY
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(*c)
        self.cell(0, 9, sanitize(title), new_x='LMARGIN', new_y='NEXT', border='B')
        self.set_text_color(*self.DARK_TEXT)
        self.ln(3)

    def body(self, text: str, size: int = 11):
        self.set_font('Helvetica', '', size)
        self.set_text_color(*self.MID_TEXT)
        self.multi_cell(0, 6, sanitize(text), new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def kv_row(self, key: str, value: str):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*self.DARK_TEXT)
        self.cell(52, 7, sanitize(key))
        self.set_font('Helvetica', '', 11)
        self.set_text_color(*self.MID_TEXT)
        self.multi_cell(0, 7, sanitize(value), new_x='LMARGIN', new_y='NEXT')

    def highlight_box(self, text: str):
        self.set_fill_color(*self.LIGHT_BG)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(*self.MID_TEXT)
        self.multi_cell(0, 6, sanitize(text), new_x='LMARGIN', new_y='NEXT', fill=True, border=1)
        self.set_text_color(*self.DARK_TEXT)
        self.ln(3)

    def match_bar(self, rank: str, career: str, pct: float, color=None):
        c = color or self.PRIMARY
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*self.DARK_TEXT)
        self.cell(90, 7, sanitize(f'{rank}  {career}'))
        self.set_font('Helvetica', '', 11)
        self.cell(35, 7, sanitize(f'{pct:.1f}% Match'))
        x, y = self.get_x(), self.get_y() + 1
        self.set_fill_color(210, 210, 210)
        self.rect(x, y, 55, 4, 'F')
        self.set_fill_color(*c)
        self.rect(x, y, max(55 * pct / 100, 1), 4, 'F')
        self.ln(9)


def build_pdf(out_path: str = 'project_summary.pdf'):
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)

    # =========================================================
    # PAGE 1 — PROJECT OVERVIEW
    # =========================================================
    pdf.add_page()

    pdf.set_fill_color(*ReportPDF.PRIMARY)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 22)
    pdf.cell(0, 18, ' KIT AI Career Recommendation Hub ', new_x='LMARGIN',
             new_y='NEXT', fill=True, align='C')
    pdf.set_font('Helvetica', '', 12)
    pdf.set_fill_color(20, 80, 180)
    pdf.cell(0, 9, '  Project Summary & Resume Analysis Report  ',
             new_x='LMARGIN', new_y='NEXT', fill=True, align='C')
    pdf.set_text_color(*ReportPDF.DARK_TEXT)
    pdf.ln(8)

    pdf.section_title('Project Purpose', ReportPDF.PRIMARY)
    pdf.body(
        'AI Career Recommendation Hub is a Python desktop application built with CustomTkinter '
        'that evaluates a student\'s aptitude via a 15-factor psychometric slider assessment, '
        'then uses a trained RandomForestClassifier to predict the best-fit career paths and '
        'Google Gemini AI to generate personalized career analysis reports. '
        'The app also includes a full-featured AI Resume Builder with live preview and PDF export.'
    )

    pdf.section_title('Architecture', ReportPDF.PRIMARY)
    pdf.body(
        'main.py         (1,559 lines) - Complete GUI, all pages, threading, PDF export\n'
        'ml_engine.py       (169 lines) - RandomForest training & prediction engine\n'
        'ai_service.py      (175 lines) - Gemini API integration with offline fallbacks\n'
        'export_summary_pdf.py          - This project summary PDF generator\n'
        'career_model.pkl / scaler.pkl  - Persisted trained model and feature scaler\n'
        '.env                           - Environment file storing GEMINI_API_KEY'
    )

    pdf.section_title('Technology Stack', ReportPDF.SECONDARY)
    pdf.kv_row('GUI Framework:',  'CustomTkinter with dark GitHub-inspired theme (1400x900)')
    pdf.kv_row('ML Model:',       'RandomForestClassifier (200 estimators, depth=15, 30 classes)')
    pdf.kv_row('Training Data:',  'Synthetic - 200 samples x 30 careers = 6,000 total samples')
    pdf.kv_row('AI Backend:',     'Google Gemini gemini-2.5-flash (structured JSON + text outputs)')
    pdf.kv_row('PDF Export:',     'fpdf2 + matplotlib (embedded bar chart)')
    pdf.kv_row('Assessment:',     '15 features: Math, Science, English, Aptitude Space, '
                                   'Technical Knack, Communication, Logical Reasoning, '
                                   'Creative Ability, Arts Interest, Science Interest, '
                                   'Commercial Awareness, Extroversion, Leadership, '
                                   'Problem Solving, Computer Science')
    pdf.ln(4)

    pdf.section_title('Key Application Features', ReportPDF.SECONDARY)
    features = [
        'Login & Registration with in-memory user database',
        'Dashboard sidebar navigation (Overview, Assessment, History, Resume Builder)',
        'Neural Assessment: 15 sliders grouped in 3 cognitive categories',
        'ML Pipeline: RandomForest inference returning Top-3 career matches with probability',
        'Gemini AI: 5-paragraph personalized career analysis (salary, growth, skills)',
        'Results Page: 3-column layout (Profile | Recommendation | Alternatives)',
        'Results History: timestamped past assessment records per user',
        'PDF Career Report: student details, ML bars, skill chart, AI analysis',
        'Resume Builder: photo upload, dynamic education/experience rows, skill tags',
        'Resume AI: Gemini-generated career objective, summary, key strengths (JSON)',
        'Resume PDF Export: formatted A4 resume with colored header block',
        'Full Offline Fallback: all AI functions work gracefully without Gemini API key',
    ]
    for feat in features:
        pdf.body(f'  * {feat}')

    # =========================================================
    # PAGE 2 — RESUME ANALYSIS: KOMAL PRIYA
    # =========================================================
    pdf.add_page()
    pdf.colored_header(
        'Student 1: Komal Priya  -  Resume Builder Analysis',
        'Resume generated using the AI Resume Builder feature of the application',
        ReportPDF.SECONDARY
    )

    pdf.section_title('Personal Information', ReportPDF.PRIMARY)
    pdf.kv_row('Name:',        'Komal Priya')
    pdf.kv_row('Email:',       'komalpriya337@gmail.com')
    pdf.kv_row('Phone:',       '+91 6204929339')
    pdf.kv_row('Location:',    'Arwal, Bihar')
    pdf.kv_row('Target Role:', 'Marketing Professional')
    pdf.kv_row('LinkedIn:',    'linkedin.com/in/komal-priya-b5a69b2b3')
    pdf.ln(3)

    pdf.section_title('AI-Generated Career Objective', ReportPDF.PRIMARY)
    pdf.highlight_box(
        'To secure a dynamic Marketing position, leveraging practical experience in marketing '
        'and business development to drive impactful campaigns and contribute significantly '
        'to organizational growth.'
    )

    pdf.section_title('AI-Generated Professional Summary', ReportPDF.PRIMARY)
    pdf.highlight_box(
        'A results-oriented Master\'s graduate with nearly a year and a half of combined '
        'experience in Marketing and Business Development. Proven ability to engage clients, '
        'drive outreach, and contribute to business growth, acquired through roles at '
        'Insplor Consultant and Ai Expert Academy. Eager to apply a comprehensive understanding '
        'of marketing principles and practical skills to execute successful campaigns and '
        'achieve strategic objectives within a dynamic marketing team.'
    )

    pdf.section_title('Key Strengths (AI-Generated)', ReportPDF.SECONDARY)
    for s in [
        'Client Relationship Management',
        'Strategic Business Development',
        'Marketing Campaign Support',
        'Effective Communication & Outreach',
    ]:
        pdf.body(f'   * {s}')

    pdf.section_title('Education', ReportPDF.PURPLE)
    for edu in [
        'Matriculation          -  Rajkiya Krit High School, Bharaoob (2016)',
        'Intermediate           -  Rajkiya Krit High School, Bharaoob (2018)',
        'Bachelor Degree        -  Sachinda Nand Shina College, Aurangabad, Bihar (2022)',
        "Master's Degree        -  Gandhi Engineering College, BBSR, Odisha (2025)",
    ]:
        pdf.body(f'   * {edu}')

    pdf.section_title('Work / Internship Experience', (200, 120, 0))
    for exp in [
        'Marketing Intern  at  Insplor Consultant                    (3 Months)',
        'Business Development Manager  at  Ai Expert Academy, BBSR   (11 Months)',
    ]:
        pdf.body(f'   * {exp}')

    pdf.section_title('Resume Quality Assessment', ReportPDF.WARN)
    pdf.body(
        'Strengths: Komal\'s resume effectively highlights her marketing and BDM experience. '
        'The AI-generated objective and summary are professional and role-specific. '
        'Good diversity of educational background from matriculation to Master\'s level.'
    )
    pdf.body(
        'Suggestions: Add quantifiable achievements (e.g., "increased outreach by 30%"). '
        'Expand the skills section with specific marketing tools (Google Ads, CRM, etc.). '
        'Consider adding a portfolio link or project descriptions for campaigns worked on.'
    )

    # =========================================================
    # PAGE 3 — CAREER PROFILE: ROHIT
    # =========================================================
    pdf.add_page()
    pdf.colored_header(
        'Student 2: Rohit  -  KIT AI Career Profile Report',
        'Career assessment result generated by the ML + Gemini pipeline',
        (40, 100, 200)
    )

    pdf.section_title('Student Details', ReportPDF.PRIMARY)
    pdf.kv_row('Full Name:',       'Rohit')
    pdf.kv_row('Username:',        'Rohit')
    pdf.kv_row('College:',         'KIT (Kalam Institute of Technology)')
    pdf.kv_row('Academic Stream:', 'Science')
    pdf.ln(4)

    pdf.section_title('Optimal Career Matches  (RandomForest ML Model)', ReportPDF.SECONDARY)
    pdf.match_bar('#1', 'Sales Manager',         33.6, ReportPDF.SECONDARY)
    pdf.match_bar('#2', 'Cybersecurity Analyst',  24.1, ReportPDF.PRIMARY)
    pdf.match_bar('#3', 'HR Specialist',           11.4, ReportPDF.PURPLE)
    pdf.ln(4)

    pdf.section_title('Notable Assessment Scores', ReportPDF.PRIMARY)
    highlights = [
        ('Computer Science',    100, 'Outstanding'),
        ('Problem Solving',      96, 'Exceptional'),
        ('Leadership',           89, 'Strong'),
        ('Extroversion',         81, 'High'),
        ('Commercial Awareness', 75, 'Good'),
        ('Communication',        30, 'Needs Improvement'),
        ('English',              16, 'Needs Improvement'),
    ]
    for trait, score, label in highlights:
        c = ReportPDF.SECONDARY if score >= 70 else ReportPDF.WARN
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(*ReportPDF.DARK_TEXT)
        pdf.cell(70, 7, sanitize(f'  {trait}:'))
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(*c)
        pdf.cell(0, 7, sanitize(f'{score}/100  ({label})'), new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(*ReportPDF.DARK_TEXT)
    pdf.ln(3)

    pdf.section_title('Gemini AI Career Analysis', ReportPDF.PRIMARY)
    pdf.body(
        'Your exceptional Problem Solving (96), Leadership (89), Extroversion (81), '
        'and perfect Computer Science (100) score make Sales Manager a highly aligned career. '
        'Your Commercial Awareness (75) adds valuable market intuition for a sales leadership role.'
    )
    pdf.body(
        'Development Areas: Communication (30) and English (16) are critical gaps. '
        'Persuasive communication is at the core of successful sales management. '
        'Focused improvement in these areas will significantly unlock your potential.'
    )

    pdf.section_title('Required Skills for Sales Manager', ReportPDF.WARN)
    for sk in [
        'Advanced Communication and Negotiation Skills',
        'Strategic Leadership and Team Building',
        'Data Analysis and CRM Proficiency',
        'Problem Solving and Adaptability in dynamic markets',
    ]:
        pdf.body(f'   * {sk}')

    pdf.section_title('Market Insights (AI)', ReportPDF.SECONDARY)
    pdf.kv_row('Salary Range:',   '$70,000 - $150,000 per year + commission / bonus structures')
    pdf.kv_row('Growth Trends:',  ('Stable to slightly increasing demand over the next decade. '
                                    'Sales Managers who can leverage data analytics, CRM tools, '
                                    'and digital channels will be in highest demand globally.'))

    # =========================================================
    # PAGE 4 — CAREER PROFILE: MOHIT
    # =========================================================
    pdf.add_page()
    pdf.colored_header(
        'Student 3: Mohit  -  KIT AI Career Profile Report',
        'Career assessment result generated by the ML + Gemini pipeline',
        (40, 100, 200)
    )

    pdf.section_title('Student Details', ReportPDF.PRIMARY)
    pdf.kv_row('Full Name:',       'Mohit')
    pdf.kv_row('Username:',        'Mohit')
    pdf.kv_row('College:',         'Kalam Institute of Technology (KIT)')
    pdf.kv_row('Academic Stream:', 'Science')
    pdf.ln(4)

    pdf.section_title('Optimal Career Matches  (RandomForest ML Model)', ReportPDF.SECONDARY)
    pdf.match_bar('#1', 'Product Manager',        16.1, ReportPDF.SECONDARY)
    pdf.match_bar('#2', 'Cybersecurity Analyst',   14.9, ReportPDF.PRIMARY)
    pdf.match_bar('#3', 'Sales Manager',            9.5, ReportPDF.PURPLE)
    pdf.ln(4)

    pdf.section_title('Notable Assessment Scores', ReportPDF.PRIMARY)
    highlights_m = [
        ('Computer Science',    100, 'Perfect'),
        ('English',             100, 'Perfect'),
        ('Extroversion',         95, 'Exceptional'),
        ('Leadership',           90, 'Strong'),
        ('Commercial Awareness', 80, 'Strong'),
        ('Problem Solving',      75, 'Good'),
        ('Creative Ability',     45, 'Needs Development'),
        ('Logical Reasoning',    50, 'Average'),
    ]
    for trait, score, label in highlights_m:
        c = ReportPDF.SECONDARY if score >= 70 else ReportPDF.WARN
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(*ReportPDF.DARK_TEXT)
        pdf.cell(70, 7, sanitize(f'  {trait}:'))
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(*c)
        pdf.cell(0, 7, sanitize(f'{score}/100  ({label})'), new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(*ReportPDF.DARK_TEXT)
    pdf.ln(3)

    pdf.section_title('Gemini AI Career Analysis', ReportPDF.PRIMARY)
    pdf.body(
        'Perfect scores in Computer Science (100) and English (100), combined with outstanding '
        'Extroversion (95) and Leadership (90), make Product Manager a natural career fit. '
        'Strong Commercial Awareness (80) and Science Interest position you well for understanding '
        'market needs and guiding development teams toward impactful product solutions.'
    )
    pdf.body(
        'Development Areas: Creative Ability (45) could be cultivated for better feature ideation '
        'and user-centered thinking. Strengthening Logical Reasoning (50) will help in dissecting '
        'complex product problems and formulating robust product-market strategies.'
    )

    pdf.section_title('Required Skills for Product Manager', ReportPDF.WARN)
    for sk in [
        'Product Vision and Strategy - roadmap definition and prioritization',
        'Stakeholder Management and Cross-functional Leadership',
        'Technical Understanding for effective engineering communication',
        'User Empathy and Market Research for impactful product decisions',
    ]:
        pdf.body(f'   * {sk}')

    pdf.section_title('Market Insights (AI)', ReportPDF.SECONDARY)
    pdf.kv_row('Salary Range:',  '$80,000 - $180,000+ annually for experienced professionals')
    pdf.kv_row('Growth Trends:', ('Exceptionally strong. As digital product development accelerates, '
                                   'demand for skilled Product Managers is projected to grow '
                                   'significantly over the next decade across all sectors.'))

    # =========================================================
    # PAGE 5 — CODE ANALYSIS & IMPROVEMENT SUGGESTIONS
    # =========================================================
    pdf.add_page()
    pdf.colored_header(
        'Code Analysis & Improvement Suggestions',
        'Technical review of the project codebase quality',
        ReportPDF.PURPLE
    )

    pdf.section_title('Code Quality Overview', ReportPDF.PRIMARY)
    pdf.kv_row('main.py (1,559 lines):',       'GUI + all pages. Well-structured but monolithic.')
    pdf.kv_row('ml_engine.py (169 lines):',    'Clean, well-documented. Excellent auto-retrain logic.')
    pdf.kv_row('ai_service.py (175 lines):',   'Best module. Typed, documented, fallback, JSON parsing.')
    pdf.kv_row('Overall Architecture:',        'Good 3-layer separation: GUI / ML / AI Service.')
    pdf.ln(3)

    pdf.section_title('[!] Critical Issues', ReportPDF.WARN)
    for title, desc in [
        ('In-Memory User Database',
         'All registered users and history are lost every time the app is closed. '
         'Fix: Persist to SQLite (built-in) or a JSON file.'),
        ('Plaintext Password Storage',
         'Passwords stored as raw strings in a Python dict. '
         'Fix: Hash with hashlib.sha256 before storing and compare hashes.'),
        ('False Model Accuracy Display',
         'The "94.6% accuracy" shown on the dashboard is training accuracy, not real accuracy. '
         'Fix: Use sklearn train_test_split and evaluate on a held-out test set.'),
    ]:
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(*ReportPDF.WARN)
        pdf.cell(0, 7, sanitize(f'  [!] {title}'), new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*ReportPDF.MID_TEXT)
        pdf.multi_cell(0, 6, sanitize(f'      {desc}'), new_x='LMARGIN', new_y='NEXT')
        pdf.ln(1)

    pdf.section_title('[~] Moderate Issues', (200, 130, 0))
    for item in [
        'import statements inside methods (slow, non-Pythonic) - move all to top of file.',
        'MLPredictor initialized at module level before GUI starts - can cause silent startup freeze.',
        'Interests section (Science High/Commerce Medium/Arts Low) is hard-coded, never changes.',
        'Default login credentials (Rohit / 1234) pre-filled in UI - remove before deployment.',
        'Two code sections are both labeled "#4" in comments - numbering error.',
    ]:
        pdf.body(f'  * {item}')

    pdf.section_title('[+] Recommended Improvements', ReportPDF.SECONDARY)
    for imp in [
        'Persist users and history to SQLite using built-in sqlite3 module (no extra dependency).',
        'Hash passwords with hashlib.sha256 before storing.',
        'Use train_test_split to evaluate model on unseen data before showing accuracy.',
        'Add a startup splash screen while model loads to prevent apparent freeze.',
        'Break main.py into page modules: login_page.py, results_page.py, resume_page.py.',
        'Add unit tests for ml_engine.predict() and ai_service fallback paths.',
        'Replace bare except: clauses with except Exception: to avoid swallowing signals.',
        'Use named FEATURES index constants instead of magic numbers like original_scores[6].',
        'Add input sanitization for registration fields (length, special characters).',
        'Cache Gemini API responses locally to reduce redundant API calls.',
    ]:
        pdf.body(f'  * {imp}')

    pdf.output(out_path)
    print(f'[OK] Project summary PDF written: {out_path}')


if __name__ == '__main__':
    build_pdf('project_summary.pdf')
