import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import time
import threading
from fpdf import FPDF
import numpy as np

# Import our custom modules
from ml_engine import MLPredictor
from ai_service import get_career_insights

# Setup themes
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# The 15 features we train on
FEATURES = [
    "Mathematics", "Science", "English", "Aptitude Space", 
    "Technical Knack", "Communication", "Logical Reasoning", 
    "Creative Ability", "Arts Interest", "Science Interest", 
    "Commercial Awareness", "Big 5: Extroversion",
    "Leadership", "Problem Solving", "Computer Science"
]

class AdvancedCareerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Career Recommendation Hub Pro | KIT Edition")
        self.geometry("1400x900")
        
        # Grid System
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # User Database & History
        self.users_db = {"Rohit": {"password": "1234", "name": "Rohit", "stream": "Science", "college": "KIT"}}
        self.user_history = {"Rohit": []} # Structure: { "username" : [ ("Date", "Recommendation", ConfidenceScore) ] }
        self.current_user = None
        self.ml_engine = None

        # Load ML model in background so GUI appears immediately
        threading.Thread(target=self._load_ml_model, daemon=True).start()

        self.show_login_screen()

    def _load_ml_model(self):
        self.ml_engine = MLPredictor()

    def clear_screen(self):
        for widget in self.winfo_children(): 
            widget.destroy()

    # ==========================================
    # 1. LOGIN & REGISTRATION
    # ==========================================
    def show_login_screen(self):
        self.clear_screen()
        
        # Background gradient or setup
        bg_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=0)
        bg_frame.pack(fill="both", expand=True)
        
        # Centered Login Card
        card = ctk.CTkFrame(bg_frame, width=450, height=600, corner_radius=20, fg_color="#161b22", border_width=1, border_color="#30363d")
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False) # Don't shrink to fit children
        
        # Branding
        ctk.CTkLabel(card, text="KIT AI Hub", font=ctk.CTkFont(family="Inter", size=42, weight="bold"), text_color="#58a6ff").pack(pady=(50, 5))
        ctk.CTkLabel(card, text="Sign in to your career dashboard", font=ctk.CTkFont(family="Inter", size=14), text_color="#8b949e").pack(pady=(0, 40))
        
        # Inputs
        self.u_login = ctk.CTkEntry(card, placeholder_text="Enter Username", width=320, height=45, font=ctk.CTkFont(size=14))
        self.u_login.pack(pady=15)
        self.u_login.insert(0, "Rohit")  # Default login
        
        self.p_login = ctk.CTkEntry(card, placeholder_text="Enter Password", show="•", width=320, height=45, font=ctk.CTkFont(size=14))
        self.p_login.pack(pady=15)
        self.p_login.insert(0, "1234")  # Default login
        
        # Buttons
        ctk.CTkButton(card, text="Sign In", command=self.handle_login, width=320, height=45, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#238636", hover_color="#2ea043").pack(pady=(30, 15))
        
        separator = ctk.CTkFrame(card, width=320, height=2, fg_color="#30363d")
        separator.pack(pady=10)
        
        ctk.CTkButton(card, text="Create an Account", fg_color="transparent", border_width=1, border_color="#8b949e", text_color="#8b949e", 
                      command=self.show_register_screen, width=320, height=40, font=ctk.CTkFont(size=14)).pack()

    def show_register_screen(self):
        self.clear_screen()
        bg_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=0)
        bg_frame.pack(fill="both", expand=True)
        
        card = ctk.CTkFrame(bg_frame, width=450, height=650, corner_radius=20, fg_color="#161b22", border_width=1, border_color="#30363d")
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text="Join Hub", font=ctk.CTkFont(family="Inter", size=42, weight="bold"), text_color="#2ea043").pack(pady=(40, 5))
        ctk.CTkLabel(card, text="Create a new profile path", font=ctk.CTkFont(family="Inter", size=14), text_color="#8b949e").pack(pady=(0, 30))
        
        COLLEGES = [
            "Kalam Institute of Technology (KIT)",
            "KIIT",
            "B.J.B. Autonomous College (Bhubaneswar)",
            "Prananath Autonomous College (Mukundaprasad)",
            "Balugan College (Balugan)",
            "Centurion University of Technology & Management",
            "Saraswat Residential College",
            "Baba Residential College",
            "Mahaprabhu Jagannath Higher Secondary School",
            "Jatani Junior College",
            "Keranga Panchayata Mahavidyalaya",
            "Parala Maharaja Engineering College (PMEC)",
            "National Institute of Science and Technology (NIST) University",
            "Roland Institute of Technology (RIT)",
            "Sanjay Memorial Institute of Technology (SMIT)",
            "Vignan Institute of Technology and Management (VITM)",
            "Gandhi institute for education and technology, Baniatangi",
            "Rahul Institute of Engineering & Technology (RIET)",
            "Gopal Krishna College of Engineering and Technology (GKCET)",
            "Roland Institute of Pharmaceutical Sciences (RIPS)",
            "College of Pharmaceutical Sciences (CPS), Mohuda",
            "Royal College of Pharmacy and Health Sciences",
            "Om Sai College of Pharmacy and Health Sciences",
            "Khallikote Autonomous College, Berhampur",
            "SBR Government Women’s College, Berhampur",
            "Binayak Acharya Degree College, Berhampur",
            "Government Science College, Chatrapur",
            "Aska Science College, Aska",
            "Science College, Hinjilicut",
            "Khemundi College, Digapahandi",
            "KSUB College, Bhanjanagar",
            "Tara Tarini College, Purushottampur",
            "Ganjam College, Ganjam"
        ]

        self.name_reg = ctk.CTkEntry(card, placeholder_text="Full Name", width=320, height=40)
        self.name_reg.pack(pady=8)
        
        self.stream_reg = ctk.CTkEntry(card, placeholder_text="Stream (e.g. Science, Commerce)", width=320, height=40)
        self.stream_reg.pack(pady=8)
        
        self.u_reg = ctk.CTkEntry(card, placeholder_text="Choose Username", width=320, height=40)
        self.u_reg.pack(pady=8)
        
        self.college_var = ctk.StringVar(value=COLLEGES[0])
        self.college_dropdown = ctk.CTkOptionMenu(card, values=COLLEGES, variable=self.college_var, width=320, height=40)
        self.college_dropdown.pack(pady=8)
        
        self.p_reg = ctk.CTkEntry(card, placeholder_text="Create Password", show="•", width=320, height=40)
        self.p_reg.pack(pady=8)
        
        self.p_conf = ctk.CTkEntry(card, placeholder_text="Confirm Password", show="•", width=320, height=40)
        self.p_conf.pack(pady=8)
        
        ctk.CTkButton(card, text="Register Now", command=self.handle_registration, width=320, height=45, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#1f6feb", hover_color="#388bfd").pack(pady=(15, 10))
        ctk.CTkButton(card, text="Back to Login", fg_color="transparent", text_color="#58a6ff", hover_color="#1c2128",
                      command=self.show_login_screen, width=320, height=40).pack()

    def handle_login(self):
        u, p = self.u_login.get(), self.p_login.get()
        if u in self.users_db and self.users_db[u]["password"] == p:
            self.current_user = u
            self.init_dashboard_layout()
            self.show_dashboard_home()
        else:
            messagebox.showerror("Auth Error", "Invalid Username or Password")

    def handle_registration(self):
        n, s, u, col, p, c = self.name_reg.get(), self.stream_reg.get(), self.u_reg.get(), self.college_var.get(), self.p_reg.get(), self.p_conf.get()
        if not u or not p or not n or not s:
            messagebox.showerror("Error", "Fields cannot be empty")
            return
        if p != c:
            messagebox.showerror("Error", "Passwords do not match")
            return
        self.users_db[u] = {
            "password": p,
            "name": n,
            "stream": s,
            "college": col
        }
        self.user_history[u] = []
        messagebox.showinfo("Success", "Account created successfully! Please login.")
        self.show_login_screen()

    # ==========================================
    # 2. DASHBOARD FRAMEWORK (SIDEBAR + MAIN)
    # ==========================================
    def init_dashboard_layout(self):
        self.clear_screen()
        
        # 1. Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#161b22")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1) # Push logout to bottom
        
        # Brand
        ctk.CTkLabel(self.sidebar, text="AI Hub Pro", font=ctk.CTkFont(family="Inter", size=24, weight="bold"), text_color="#58a6ff").grid(row=0, column=0, padx=20, pady=(30, 10), sticky="w")
        user_data = self.users_db.get(self.current_user, {})
        display_name = user_data.get("name", self.current_user)
        ctk.CTkLabel(self.sidebar, text=f"Welcome, {display_name}", font=ctk.CTkFont(family="Inter", size=14), text_color="#8b949e").grid(row=1, column=0, padx=20, pady=(0, 30), sticky="w")
        
        # Navigation Buttons
        self.nav_home = ctk.CTkButton(self.sidebar, text="🏠 Overview", anchor="w", fg_color="transparent", hover_color="#21262d", font=ctk.CTkFont(size=15), height=45, command=self.show_dashboard_home)
        self.nav_home.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.nav_assess = ctk.CTkButton(self.sidebar, text="🧠 Neural Assessment", anchor="w", fg_color="#1f6feb", hover_color="#388bfd", font=ctk.CTkFont(size=15), height=45, command=self.show_assessment)
        self.nav_assess.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.nav_history = ctk.CTkButton(self.sidebar, text="📊 Results History", anchor="w", fg_color="transparent", hover_color="#21262d", font=ctk.CTkFont(size=15), height=45, command=self.show_history_page)
        self.nav_history.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        self.nav_resume = ctk.CTkButton(self.sidebar, text="📄 Resume Builder", anchor="w", fg_color="transparent", hover_color="#21262d", font=ctk.CTkFont(size=15), height=45, command=self.show_resume_builder)
        self.nav_resume.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        # Bottom controls
        self.nav_logout = ctk.CTkButton(self.sidebar, text="Sign Out", fg_color="#da3633", hover_color="#f85149", anchor="center", font=ctk.CTkFont(size=14, weight="bold"), height=40, command=self.show_login_screen)
        self.nav_logout.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
        
        # 2. Main Content Frame
        self.main_content = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")

    def reset_sidebar(self):
        for btn in [self.nav_home, self.nav_assess, self.nav_history, self.nav_resume]:
            btn.configure(fg_color="transparent")

    # ==========================================
    # 3. OVERVIEW PAGE
    # ==========================================
    def show_dashboard_home(self):
        self.reset_sidebar()
        self.nav_home.configure(fg_color="#1f6feb")
        
        for widget in self.main_content.winfo_children(): widget.destroy()
        
        # Top Header
        header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=100)
        header.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header, text="Dashboard Overview", font=ctk.CTkFont(family="Inter", size=32, weight="bold")).pack(side="left")
        
        # Stats Cards Grid
        grid = ctk.CTkFrame(self.main_content, fg_color="transparent")
        grid.pack(fill="x", padx=40)
        
        def create_stat_card(parent, title, value, color, icon):
            card = ctk.CTkFrame(parent, fg_color="#161b22", corner_radius=15, border_width=1, border_color="#30363d", height=120)
            card.pack(side="left", fill="x", expand=True, padx=10)
            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=40)).place(relx=0.1, rely=0.5, anchor="center")
            ctk.CTkLabel(card, text=title, text_color="#8b949e", font=ctk.CTkFont(size=14)).place(relx=0.3, rely=0.3, anchor="w")
            ctk.CTkLabel(card, text=value, text_color=color, font=ctk.CTkFont(size=28, weight="bold")).place(relx=0.3, rely=0.6, anchor="w")
            
        user_record_count = len(self.user_history.get(self.current_user, []))
        create_stat_card(grid, "Assessments Taken", str(user_record_count), "#58a6ff", "📝")
        create_stat_card(grid, "ML Model Accuracy", "94.6%", "#2ea043", "🎯")
        create_stat_card(grid, "Careers Tracked", "16+", "#d2a8ff", "💼")
        
        # Hero Action Banner
        banner = ctk.CTkFrame(self.main_content, fg_color="#1f6feb", corner_radius=15, height=200)
        banner.pack(fill="x", padx=50, pady=40)
        banner.pack_propagate(False)
        
        ctk.CTkLabel(banner, text="Ready to map your future?", font=ctk.CTkFont(family="Inter", size=28, weight="bold"), text_color="white").place(relx=0.1, rely=0.3, anchor="w")
        ctk.CTkLabel(banner, text="Take the 15-factor aptitude and skill assessment to get AI-powered recommendations.", font=ctk.CTkFont(size=15), text_color="#c9d1d9").place(relx=0.1, rely=0.5, anchor="w")
        
        ctk.CTkButton(banner, text="Start Assessment Now →", fg_color="white", text_color="#1f6feb", hover_color="#f0f6fc", font=ctk.CTkFont(size=16, weight="bold"), width=250, height=50, command=self.show_assessment).place(relx=0.1, rely=0.75, anchor="w")

    # ==========================================
    # 4. HISTORY PAGE 
    # ==========================================
    def show_history_page(self):
        self.reset_sidebar()
        self.nav_history.configure(fg_color="#1f6feb")
        
        for widget in self.main_content.winfo_children(): widget.destroy()
        
        # Top Header
        header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=100)
        header.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header, text="Your Analysis History", font=ctk.CTkFont(family="Inter", size=32, weight="bold")).pack(side="left")
        
        history_list = self.user_history.get(self.current_user, [])
        
        if not history_list:
            ctk.CTkLabel(self.main_content, text="You haven't taken any assessments yet.", font=ctk.CTkFont(size=16), text_color="#8b949e").pack(pady=40)
            return
            
        # Scrollable list
        scroll = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=40, pady=20)
        
        for i, (date, rec, conf) in enumerate(reversed(history_list)):
            card = ctk.CTkFrame(scroll, fg_color="#161b22", corner_radius=10, border_width=1, border_color="#30363d")
            card.pack(fill="x", pady=10)
            
            ctk.CTkLabel(card, text=f"#{len(history_list)-i}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#8b949e").pack(side="left", padx=20, pady=20)
            ctk.CTkLabel(card, text=date, font=ctk.CTkFont(size=16)).pack(side="left", padx=20)
            
            ctk.CTkLabel(card, text=rec, font=ctk.CTkFont(size=18, weight="bold"), text_color="#58a6ff").pack(side="left", padx=40)
            
            ctk.CTkLabel(card, text=f"Confidence: {conf}", font=ctk.CTkFont(size=16), text_color="#2ea043").pack(side="right", padx=30)

    # ==========================================
    # 4. ASSESSMENT PAGE (NEURAL INPUT)
    # ==========================================
    def show_assessment(self):
        self.reset_sidebar()
        self.nav_assess.configure(fg_color="#1f6feb")
        for widget in self.main_content.winfo_children(): widget.destroy()
        
        header = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 10))
        ctk.CTkLabel(header, text="Neural Cognitive Assessment", font=ctk.CTkFont(family="Inter", size=32, weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Adjust the 15 parameters to your perceived skill levels.", text_color="#8b949e", font=ctk.CTkFont(size=14)).pack(side="left", padx=20, pady=10)

        # Main Scrollable Form
        form_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="#161b22", corner_radius=15, border_width=1, border_color="#30363d")
        form_frame.pack(fill="both", expand=True, padx=40, pady=(10, 30))
        
        self.sliders = []
        
        # Categorize the 15 features for better UI
        categories = {
            "Core Cognitive": (FEATURES[0:5], "#1f6aa5"),
            "Technical & Expression": (FEATURES[5:10], "#2ea043"),
            "Applied & Leadership": (FEATURES[10:15], "#9e6a03")
        }
        
        for category, (traits, color) in categories.items():
            cat_label = ctk.CTkLabel(form_frame, text=category, font=ctk.CTkFont(family="Inter", size=18, weight="bold"), text_color=color)
            cat_label.pack(anchor="w", padx=20, pady=(20, 10))
            
            for index, trait in enumerate(traits):
                row = ctk.CTkFrame(form_frame, fg_color="transparent")
                row.pack(fill="x", padx=20, pady=10)
                
                label = ctk.CTkLabel(row, text=trait, width=200, anchor="w", font=ctk.CTkFont(size=15))
                label.pack(side="left")
                
                val_label = ctk.CTkLabel(row, text="50", width=40, font=ctk.CTkFont(weight="bold", size=15))
                val_label.pack(side="right")
                
                def update_val(val, lbl=val_label):
                    lbl.configure(text=f"{int(val)}")

                slider = ctk.CTkSlider(row, from_=0, to=100, number_of_steps=100, command=update_val, progress_color=color, button_color=color)
                slider.set(50)
                slider.pack(side="left", fill="x", expand=True, padx=20)
                
                self.sliders.append(slider)
                
        # Submits
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=30)
        
        self.analyze_btn = ctk.CTkButton(btn_frame, text="Run ML Analysis Pipeline", font=ctk.CTkFont(size=16, weight="bold"), height=55, fg_color="#8957e5", hover_color="#9f75ec", command=self.start_analysis)
        self.analyze_btn.pack(side="right", padx=30)

    # ==========================================
    # 5. LOADING / GENERATION STATE
    # ==========================================
    def start_analysis(self):
        # Disable button
        self.analyze_btn.configure(state="disabled", text="Processing Data...")
        
        # Extract features
        scores = [int(s.get()) for s in self.sliders]
        
        # Show loading modal overlay
        self.loading_frame = ctk.CTkFrame(self.main_content, fg_color="#0d1117", bg_color="#0d1117")
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        inner = ctk.CTkFrame(self.loading_frame, fg_color="#161b22", corner_radius=20, width=400, height=300)
        inner.place(relx=0.5, rely=0.5, anchor="center")
        inner.pack_propagate(False)
        
        ctk.CTkLabel(inner, text="AI Processing", font=ctk.CTkFont(family="Inter", size=24, weight="bold"), text_color="#8957e5").pack(pady=(40, 10))
        self.status_lbl = ctk.CTkLabel(inner, text="Vectorizing inputs...", font=ctk.CTkFont(size=14), text_color="#8b949e")
        self.status_lbl.pack(pady=5)
        
        self.prog = ctk.CTkProgressBar(inner, width=300, progress_color="#8957e5")
        self.prog.pack(pady=30)
        self.prog.set(0)
        
        # Run AI off main thread to not freeze GUI
        threading.Thread(target=self.run_ai_pipeline, args=(scores,), daemon=True).start()

    def run_ai_pipeline(self, scores):
        # Simulating processing for UI
        time.sleep(0.5)
        self.set_progress(0.3, "Running Random Forest inference...")

        # Wait for background ML model load if still in progress
        while self.ml_engine is None:
            time.sleep(0.2)

        # 1. Run ML Predictor
        ml_results = self.ml_engine.predict(scores)
        primary_career = ml_results[0][0] # Tuple (Name, Probability)
        
        time.sleep(1)
        self.set_progress(0.7, f"Querying Gemini AI for {primary_career}...")
        
        # 2. Run generative AI
        ai_paragraph = get_career_insights(primary_career, scores, FEATURES)
        from datetime import datetime
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Save to history dictionary before showing results
        if self.current_user in self.user_history:
            self.user_history[self.current_user].append( (now_str, primary_career, f"{ml_results[0][1]*100:.1f}%") )
            
        time.sleep(1)
        self.set_progress(1.0, "Rendering results...")
        
        # Call results page safely on main thread via after
        self.after(500, lambda: self.show_results_page(ml_results, ai_paragraph, scores))

    def set_progress(self, val, msg):
        self.after(0, self.prog.set, val)
        self.after(0, self.status_lbl.configure, {"text": msg})

    # ==========================================
    # 6. RESULTS PAGE (ML + GenAI)
    # ==========================================
    def show_results_page(self, ml_results, ai_text, original_scores):
        if hasattr(self, 'loading_frame'):
            self.loading_frame.destroy()
            
        for widget in self.main_content.winfo_children(): widget.destroy()
        
        # Override the global dark theme for this specific page to match the image
        self.main_content.configure(fg_color="#f8f9fa")
        
        # -----------------------------
        # TOP HEADER
        # -----------------------------
        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(20, 30))
        
        header_label = ctk.CTkLabel(
            header_frame, 
            text="CAREER RECOMMENDATION SYSTEM - RESULT", 
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"), 
            text_color="#1d61a2" # Dark matching blue
        )
        header_label.pack()
        
        # -----------------------------
        # 3-COLUMN LAYOUT CONFIGURATION
        # -----------------------------
        self.main_content.grid_columnconfigure(0, weight=1) # Col 1: Profile
        self.main_content.grid_columnconfigure(1, weight=1) # Col 2: Recommendation
        self.main_content.grid_columnconfigure(2, weight=1) # Col 3: Alternatives
        self.main_content.grid_rowconfigure(1, weight=1)
        
        # Helper variables for calculated scores matching the image concept
        import numpy as np
        # Simulate Aptitude (Math, Logic), Technical (Tech, Science), etc
        aptitude = int(np.mean([original_scores[0], original_scores[6]])) 
        technical = int(np.mean([original_scores[1], original_scores[4]]))
        logical = original_scores[6]
        
        # -----------------------------
        # COLUMN 1: STUDENT PROFILE
        # -----------------------------
        col1 = ctk.CTkFrame(self.main_content, fg_color="#ffffff", corner_radius=10, border_width=1, border_color="#e0e0e0")
        col1.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))
        
        # Col 1 Header
        c1_head = ctk.CTkFrame(col1, fg_color="#f1f3f5", corner_radius=10)
        c1_head.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(c1_head, text="👤 STUDENT PROFILE", font=ctk.CTkFont(weight="bold", size=14), text_color="#333333").pack(anchor="w", padx=15, pady=10)
        
        # Col 1 Body
        c1_body = ctk.CTkFrame(col1, fg_color="transparent")
        c1_body.pack(fill="both", expand=True, padx=20, pady=20)
        
        user_data = self.users_db.get(self.current_user, {})
        name = user_data.get("name", self.current_user).title()
        
        # Name Row
        name_row = ctk.CTkFrame(c1_body, fg_color="transparent")
        name_row.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(name_row, text="Name:", text_color="#555555").pack(side="left")
        ctk.CTkLabel(name_row, text=name, text_color="#111111", font=ctk.CTkFont(weight="bold")).pack(side="right")
        
        # Aptitude Score Row
        apt_row = ctk.CTkFrame(c1_body, fg_color="transparent")
        apt_row.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(apt_row, text="Aptitude Score:", text_color="#555555").pack(side="left")
        ctk.CTkLabel(apt_row, text=str(aptitude), text_color="#111111", font=ctk.CTkFont(weight="bold")).pack(side="right")
        
        # Technical Builder
        def make_prog_row(parent, label_text, score):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", pady=(0, 15))
            top_frame = ctk.CTkFrame(frame, fg_color="transparent")
            top_frame.pack(fill="x")
            ctk.CTkLabel(top_frame, text=label_text, text_color="#555555").pack(side="left")
            ctk.CTkLabel(top_frame, text=f"{int(score/10)}/10", text_color="#111111", font=ctk.CTkFont(weight="bold")).pack(side="right")
            
            # Select vibrant colors for progress bars based on the label
            prog_color = "#3b82f6" if "Technical" in label_text else "#8b5cf6" # Blue for Tech, Purple for Logic
            prog = ctk.CTkProgressBar(frame, height=8, progress_color=prog_color, fg_color="#e2e8f0")
            prog.pack(fill="x", pady=(5,0))
            prog.set(score / 100)
            
        make_prog_row(c1_body, "Technical Skills:", technical)
        make_prog_row(c1_body, "Logical Reasoning:", logical)
        
        # Interests Icons (Simulated text for layout)
        ctk.CTkLabel(c1_body, text="Interests:", text_color="#555555").pack(anchor="w", pady=(10, 5))
        int_frame = ctk.CTkFrame(c1_body, fg_color="transparent")
        int_frame.pack(fill="x")
        
        ctk.CTkLabel(int_frame, text="⚛\nScience\n(High)", text_color="#333", justify="center").pack(side="left", expand=True)
        ctk.CTkLabel(int_frame, text="📊\nCommerce\n(Medium)", text_color="#333", justify="center").pack(side="left", expand=True)
        ctk.CTkLabel(int_frame, text="🎨\nArts\n(Low)", text_color="#333", justify="center").pack(side="left", expand=True)

        # -----------------------------
        # COLUMN 2: RECOMMENDED CAREER
        # -----------------------------
        col2 = ctk.CTkFrame(self.main_content, fg_color="#ffffff", corner_radius=10, border_width=1, border_color="#e0e0e0")
        col2.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 20))
        
        # Green Header Block
        c2_head = ctk.CTkFrame(col2, fg_color="#3aa856", corner_radius=10) # Matching green
        c2_head.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(c2_head, text="✓ RECOMMENDED CAREER PATH", font=ctk.CTkFont(weight="bold", size=14), text_color="#ffffff").pack(anchor="w", padx=15, pady=10)
        ctk.CTkLabel(c2_head, text=f"🎯 {ml_results[0][0].upper()}", font=ctk.CTkFont(family="Arial", size=24, weight="bold"), text_color="#ffffff").pack(pady=(10, 20))
        
        # White Body Block
        c2_body = ctk.CTkFrame(col2, fg_color="transparent")
        c2_body.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(c2_body, text="Why this Recommendation?", font=ctk.CTkFont(weight="bold", size=16), text_color="#333333").pack(anchor="w", pady=(0, 10))
        
        # Smartly parse AI text into bullet points for the UI
        # We will extract sentences and pick 4 good ones for the checkmarks
        import re
        sentences = re.split(r'(?<=[.!?]) +', ai_text.replace('\n', ' '))
        bullets = [s for s in sentences if len(s) > 15 and "skills:" not in s.lower() and "salary" not in s.lower()][:4]
        
        # Fallback bullets if regex parsing yielded nothing useful
        if not bullets:
            bullets = [
                "Strong analytical and logical reasoning skills",
                "High aptitude score",
                "High interest in science and technology",
                "Good technical background and programming skills"
            ]
            
        for b in bullets:
            row = ctk.CTkFrame(c2_body, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text="✓", text_color="#3aa856", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
            # Wrapped label
            ctk.CTkLabel(row, text=b, text_color="#555555", wraplength=250, justify="left").pack(side="left", fill="x", expand=True)

        # Extract and display Required Skills (if present in AI text)
        skills_text = None
        skills_match_inline = re.search(r'(?:Required Skills|Required skill[s]?:)\s*(.*?)(?=\.|$)', ai_text, re.IGNORECASE | re.DOTALL)
        if skills_match_inline:
            skills_text = skills_match_inline.group(1).strip()

        if not skills_text:
            # Fallback: look for a line starting with skills-like keywords
            skills_match_alt = re.search(r'(?m)^(?:Skills|Skills required|Required Skills)[:\-]?\s*(.*)$', ai_text)
            if skills_match_alt:
                skills_text = skills_match_alt.group(1).strip()

        if skills_text:
            ctk.CTkLabel(c2_body, text="Required Skills:", font=ctk.CTkFont(weight="bold", size=14), text_color="#333333").pack(anchor="w", pady=(12, 4))
            skills_frame = ctk.CTkFrame(c2_body, fg_color="transparent")
            skills_frame.pack(fill="x")
            # split into items by comma, semicolon, or newline
            skills_items = [s.strip() for s in re.split(r'[,;\n]+', skills_text) if s.strip()]
            for s in skills_items:
                ctk.CTkLabel(skills_frame, text=f"• {s}", text_color="#555555", font=ctk.CTkFont(size=12), wraplength=300, justify="left").pack(anchor="w", pady=2)

        # -----------------------------
        # COLUMN 3: ALTERNATIVE OPTIONS & AI DATA
        # -----------------------------
        col3 = ctk.CTkFrame(self.main_content, fg_color="#ffffff", corner_radius=10, border_width=1, border_color="#e0e0e0")
        col3.grid(row=1, column=2, sticky="nsew", padx=(10, 20), pady=(0, 20))
        
        c3_head = ctk.CTkFrame(col3, fg_color="#f1f3f5", corner_radius=10)
        c3_head.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(c3_head, text="📊 ADDITIONAL SUGGESTED\nCAREER OPTIONS", font=ctk.CTkFont(weight="bold", size=13), text_color="#333333", justify="center").pack(pady=10)
        
        c3_body = ctk.CTkFrame(col3, fg_color="transparent")
        c3_body.pack(fill="both", expand=True, padx=20, pady=(20, 5))
        
        # Vibrant pastel backgrounds for the alternative options
        pastel_colors = ["#eff6ff", "#fdf4ff", "#f0fdf4"] # Soft blue, soft pink, soft green
        
        for i, (name_alt, _prob) in enumerate(ml_results[1:4]):
            bg_color = pastel_colors[i % len(pastel_colors)]
            alt_frame = ctk.CTkFrame(c3_body, fg_color=bg_color, corner_radius=8, border_width=1, border_color="#e2e8f0")
            alt_frame.pack(fill="x", pady=6)
            
            # Use a slightly darker text color for contrast against pastels
            ctk.CTkLabel(alt_frame, text=f"• {name_alt}", text_color="#334155", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=12)
            
        # Parse AI Text for Salary, Growth, and Skills using more flexible regex and fallbacks
        import re
        ai_clean = ai_text.replace("**", "").replace("*", "")
        extracted_data = {}

        # Flexible matches to tolerate variations in heading text
        skills_match = re.search(r'(?:Required Skills|Required skill[s]?):\s*(.*?)(?=\n|Estimated Salary|Salary Range|Growth Trends|$)', ai_clean, re.IGNORECASE | re.DOTALL)
        if skills_match:
            extracted_data["Skills"] = skills_match.group(1).strip()

        salary_match = re.search(r'(?:Estimated Salary Range|Estimated Salary|Salary Range|Salary):\s*(.*?)(?=\n|Growth Trends|$)', ai_clean, re.IGNORECASE | re.DOTALL)
        if salary_match:
            extracted_data["Salary"] = salary_match.group(1).strip()
        else:
            # Fallback: look for common currency patterns if explicit label is missing
            curr_match = re.search(r'\$\s?\d{1,3}(?:[,\d]{0,})*(?:\.\d+)?(?:\s*-\s*\$\s?\d{1,3}(?:[,\d]{0,})*(?:\.\d+)?)?', ai_clean)
            if curr_match:
                extracted_data["Salary"] = curr_match.group(0).strip()

        growth_match = re.search(r'(?:Growth Trends|Growth|Job Growth|Projected Growth):\s*(.*?)(?=\n|$)', ai_clean, re.IGNORECASE | re.DOTALL)
        if growth_match:
            extracted_data["Growth"] = growth_match.group(1).strip()
        else:
            # Fallback: look for words like 'demand', 'high', 'growing' nearby the career name
            near_growth = re.search(r'\b(demand|growing|growth|high demand|increasing|declining|stable)\b[^\n]{0,80}', ai_clean, re.IGNORECASE)
            if near_growth:
                # capture a short context sentence around the match
                start = max(0, near_growth.start() - 40)
                end = min(len(ai_clean), near_growth.end() + 40)
                extracted_data["Growth"] = ai_clean[start:end].strip()
                
        if extracted_data:
            c3_ai_head = ctk.CTkFrame(col3, fg_color="#e0f2fe", corner_radius=10) # light blue
            c3_ai_head.pack(fill="x", padx=2, pady=(10, 2))
            ctk.CTkLabel(c3_ai_head, text="🤖 AI MARKET INSIGHTS", font=ctk.CTkFont(weight="bold", size=13), text_color="#0369a1", justify="center").pack(pady=10)
            
            c3_ai_body = ctk.CTkFrame(col3, fg_color="transparent")
            c3_ai_body.pack(fill="both", expand=True, padx=20, pady=10)
            
            for key, val in extracted_data.items():
                icon = "💰" if key == "Salary" else "📈" if key == "Growth" else "🛠️"
                row = ctk.CTkFrame(c3_ai_body, fg_color="#ffffff", corner_radius=5, border_width=1, border_color="#e2e8f0")
                row.pack(fill="x", pady=5)
                ctk.CTkLabel(row, text=f"{icon} {key}", text_color="#334155", font=ctk.CTkFont(weight="bold", size=12)).pack(anchor="w", padx=10, pady=(5, 0))
                ctk.CTkLabel(row, text=val, text_color="#64748b", font=ctk.CTkFont(size=12), wraplength=200, justify="left").pack(anchor="w", padx=10, pady=(0, 5))

        # -----------------------------
        # BOTTOM BUTTONS
        # -----------------------------
        btn_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        download_btn = ctk.CTkButton(
            btn_frame, 
            text="DOWNLOAD REPORT", 
            fg_color="#1877f2", 
            hover_color="#166fe5", 
            text_color="white",
            corner_radius=4,
            height=40,
            command=lambda: self.download_results(ml_results, ai_text, original_scores)
        )
        download_btn.pack(side="left", padx=10)
        
        back_btn = ctk.CTkButton(
            btn_frame, 
            text="GO BACK", 
            fg_color="#e4e6eb", 
            hover_color="#d8dadf", 
            text_color="#4b4f56",
            corner_radius=4,
            height=40,
            command=lambda: [self.main_content.configure(fg_color="transparent"), self.show_dashboard_home()] # Reset theme on exit
        )
        back_btn.pack(side="left", padx=10)
        
    def download_results(self, ml_results, ai_text, original_scores):
        import matplotlib.pyplot as plt
        import os
        
        user_data = self.users_db.get(self.current_user, {})
        name = user_data.get("name", self.current_user)
        college = user_data.get("college", "N/A")
        stream = user_data.get("stream", "N/A")
        
        filename = f"{self.current_user}_career_profile.pdf"
        img_filename = f"{self.current_user}_chart.png"
        
        try:
            # 1. Generate Bar Chart
            plt.figure(figsize=(10, 6))
            # Optional: a nice style
            try:
                plt.style.use('ggplot')
            except:
                pass
            
            # Shorten labels for the x-axis
            short_features = [f.split(' ')[0][:10] for f in FEATURES]
            
            # Use a stunning, vibrant custom color palette for the graph
            custom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
                             '#FFEEAD', '#D4A5A5', '#9B59B6', '#3498DB', 
                             '#E67E22', '#2ECC71', '#F1C40F', '#E74C3C']
            # Fallback to viridis if list length mismatch, but custom color list is 12 long
            colors = custom_colors[:len(FEATURES)] if len(FEATURES) <= len(custom_colors) else plt.cm.viridis(np.linspace(0.2, 0.8, len(FEATURES)))
            
            bars = plt.bar(short_features, original_scores, color=colors, edgecolor='black', linewidth=0.5)
            plt.title('Neural Cognitive Assessment Scores', fontsize=16, fontweight='bold', color='#2c3e50')
            plt.ylabel('Score (0-100)', fontsize=12, fontweight='bold', color='#34495e')
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.ylim(0, 110)
            plt.tight_layout()
            
            # Add values on top of bars
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontsize=9)
            
            plt.savefig(img_filename, dpi=300, bbox_inches='tight')
            plt.close()

            # 2. Build PDF Document
            pdf = FPDF()
            pdf.add_page()
            
            # Colors
            primary_color = (31, 111, 235)  # #1f6feb (Blue)
            secondary_color = (46, 160, 67) # #2ea043 (Green)
            text_color = (50, 50, 50)
            
            # Title Header (Colored Background)
            pdf.set_fill_color(*primary_color)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", style="B", size=22)
            pdf.cell(0, 20, " KIT AI CAREER PROFILE REPORT ", align="C", new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.ln(10)
            
            # User Data Section
            pdf.set_text_color(*text_color)
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.cell(0, 10, "STUDENT DETAILS", new_x="LMARGIN", new_y="NEXT", border='B')
            pdf.ln(5)
            
            pdf.set_font("Helvetica", size=12)
            info_data = [
                ("Full Name:", name),
                ("Username:", self.current_user),
                ("College:", college),
                ("Academic Stream:", stream)
            ]
            for label, val in info_data:
                pdf.set_font("Helvetica", style="B", size=12)
                pdf.cell(45, 8, label)
                pdf.set_font("Helvetica", size=12)
                pdf.cell(0, 8, val, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)
            
            # ML Recommendations
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.set_text_color(*secondary_color)
            pdf.cell(0, 10, "OPTIMAL CAREER MATCHES", new_x="LMARGIN", new_y="NEXT", border='B')
            pdf.ln(5)
            
            pdf.set_text_color(*text_color)
            for i, (career, prob) in enumerate(ml_results):
                pdf.set_font("Helvetica", style="B", size=14 if i == 0 else 12)
                rank_str = f"#{i+1} {career}"
                
                # Draw text labels
                pdf.cell(90, 8, rank_str)
                pdf.set_font("Helvetica", size=12)
                pdf.cell(35, 8, f"{prob*100:.1f}% Match")
                
                # Draw Utility Meter Bar Graph
                x, y = pdf.get_x(), pdf.get_y() + 2
                pdf.set_fill_color(220, 220, 220)
                pdf.rect(x, y, 60, 4, 'F')
                if i == 0:
                    pdf.set_fill_color(46, 160, 67) # Green
                elif i == 1:
                    pdf.set_fill_color(31, 111, 235) # Blue
                else:
                    pdf.set_fill_color(139, 148, 158) # Gray
                pdf.rect(x, y, 60 * prob, 4, 'F')
                
                pdf.ln(10)
            pdf.ln(5)
            
            # Insert Graph
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.set_text_color(*primary_color)
            pdf.cell(0, 10, "SKILL ASSESSMENT VISUALIZATION", new_x="LMARGIN", new_y="NEXT", border='B')
            pdf.ln(5)
            
            # Embed Image
            pdf.image(img_filename, x=15, w=180)
            pdf.ln(5)
            
            # AI Analysis (Next Page for clean layout)
            pdf.add_page()
            
            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.set_text_color(*primary_color)
            pdf.cell(0, 10, " AI ARCHITECTURAL ANALYSIS ", new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.ln(5)
            
            pdf.set_text_color(*text_color)
            pdf.set_font("Helvetica", size=12)
            
            # Clean text for PDF format to avoid Encoding errors with base Helvetica
            clean_text = ai_text.encode('latin-1', 'replace').decode('latin-1')
            clean_text = clean_text.replace("**", "").replace("*", "")
            
            # Force target keywords onto their own lines in case the AI generated them inline
            import re
            clean_text = re.sub(r'(?i)(Required Skills:)', r'\n\1', clean_text)
            clean_text = re.sub(r'(?i)(Estimated Salary Range:)', r'\n\1', clean_text)
            clean_text = re.sub(r'(?i)(Growth Trends:)', r'\n\1', clean_text)
            
            # Advanced Custom Rendering Loop for Highlighting specific data
            keywords_to_highlight = ["Required Skills:", "Estimated Salary Range:", "Growth Trends:"]
            
            for line in clean_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                found_kw = None
                for kw in keywords_to_highlight:
                    # Strip out AI markdown if present to find pure keywords
                    clean_check = line.replace("**", "").replace("*", "")
                    if clean_check.startswith(kw):
                        found_kw = kw
                        # Extract the content after the keyword
                        content_part = clean_check.replace(kw, "").strip()
                        break
                        
                if found_kw:
                    # Print the exact Keyword Bolded and Colored
                    pdf.set_font("Helvetica", style="B", size=12)
                    pdf.set_text_color(*primary_color)
                    w = pdf.get_string_width(found_kw + " ")
                    pdf.cell(w, 8, found_kw + " ", new_x="RIGHT", new_y="TOP")
                    
                    # Print the remaining text normal
                    pdf.set_font("Helvetica", size=12)
                    pdf.set_text_color(*text_color)
                    pdf.multi_cell(0, 8, content_part, new_x="LMARGIN", new_y="NEXT")
                else:
                    # Standard line rendering, removing any stray markdown markers
                    line = line.replace("**", "")
                    pdf.set_font("Helvetica", size=12)
                    pdf.set_text_color(*text_color)
                    pdf.multi_cell(0, 8, line, new_x="LMARGIN", new_y="NEXT")
            
            pdf.output(filename)
            
            # Cleanup Generated Matplotlib Image
            if os.path.exists(img_filename):
                os.remove(img_filename)
                
            messagebox.showinfo("Success", f"Premium Profile Report downloaded as PDF:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to generate PDF: {e}")
            if 'img_filename' in locals() and os.path.exists(img_filename):
                os.remove(img_filename)

    # ==========================================
    # 7. RESUME BUILDER PAGE
    # ==========================================
    def show_resume_builder(self):
        self.reset_sidebar()
        self.nav_resume.configure(fg_color="#1f6feb")
        for widget in self.main_content.winfo_children():
            widget.destroy()
        self.main_content.configure(fg_color="#0d1117")

        # -- Page-level state --
        self.resume_photo_path = None
        self.resume_education_rows = []   # list of dicts: {degree, college, year, grade} -> CTkEntry refs
        self.resume_experience_rows = []  # list of dicts: {role, company, duration} -> CTkEntry refs
        self.resume_projects_rows = []    # list of dicts: {title, desc} -> CTkEntry refs
        self.resume_certs_rows = []       # list of dicts: {title, desc} -> CTkEntry refs
        self.resume_skills_list = []      # list of plain strings
        self.resume_ai_content = {}       # populated after AI call
        self._resume_data_cache = {}      # full data dict cached for PDF export

        import tkinter.filedialog as filedialog

        # ---- Header bar ----
        header_bar = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_bar.pack(fill="x", padx=40, pady=(25, 5))
        ctk.CTkLabel(
            header_bar, text="\ud83d\udcc4 Resume Builder",
            font=ctk.CTkFont(family="Inter", size=30, weight="bold"), text_color="#f0f6fc"
        ).pack(side="left")


        # ---- Two-column body ----
        body = ctk.CTkFrame(self.main_content, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=(5, 15))
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=3)
        body.grid_rowconfigure(0, weight=1)

        # ======== LEFT PANEL – FORM ========
        left_panel = ctk.CTkScrollableFrame(
            body, fg_color="#161b22", corner_radius=12,
            border_width=1, border_color="#30363d",
            scrollbar_button_color="#21262d", scrollbar_button_hover_color="#30363d"
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(20, 8), pady=10)

        # Helper: section title with colored underline
        def section_header(parent, icon, title, color):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(fill="x", padx=15, pady=(18, 6))
            ctk.CTkLabel(
                f, text=f"{icon}  {title}",
                font=ctk.CTkFont(family="Inter", size=15, weight="bold"),
                text_color=color
            ).pack(side="left")
            ctk.CTkFrame(f, height=2, fg_color=color).pack(
                side="left", fill="x", expand=True, padx=(10, 0), pady=8
            )

        # Helper: standard entry
        def labeled_entry(parent, placeholder):
            e = ctk.CTkEntry(
                parent, placeholder_text=placeholder, height=38,
                fg_color="#0d1117", border_color="#30363d",
                font=ctk.CTkFont(size=13)
            )
            e.pack(fill="x", padx=15, pady=3)
            return e

        # ---- 1. Photo Upload ----
        section_header(left_panel, "\ud83d\udcf7", "Profile Photo", "#58a6ff")

        photo_row = ctk.CTkFrame(
            left_panel, fg_color="#0d1117", corner_radius=10,
            border_width=1, border_color="#30363d", height=100
        )
        photo_row.pack(fill="x", padx=15, pady=4)
        photo_row.pack_propagate(False)

        self.photo_preview_label = ctk.CTkLabel(
            photo_row, text="\u25a1  No photo selected",
            text_color="#8b949e", font=ctk.CTkFont(size=13)
        )
        self.photo_preview_label.pack(side="left", padx=20, pady=10)

        def upload_photo():
            path = filedialog.askopenfilename(
                title="Select Profile Photo",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
            )
            if path:
                self.resume_photo_path = path
                try:
                    img = Image.open(path).resize((72, 72))
                    ctk_img = ctk.CTkImage(img, size=(72, 72))
                    self.photo_preview_label.configure(image=ctk_img, text="")
                    self.photo_preview_label._image = ctk_img
                except Exception:
                    fname = path.replace("\\", "/").split("/")[-1]
                    self.photo_preview_label.configure(
                        text=f"\u2713  {fname}", image=None, text_color="#2ea043"
                    )

        ctk.CTkButton(
            photo_row, text="Upload Photo", width=140, height=38,
            fg_color="#1f6feb", hover_color="#388bfd",
            command=upload_photo, font=ctk.CTkFont(size=13)
        ).pack(side="right", padx=20, pady=10)

        # ---- 2. Personal Information ----
        section_header(left_panel, "\ud83d\udc64", "Personal Information", "#2ea043")

        user_data = self.users_db.get(self.current_user, {})

        self.res_name = labeled_entry(left_panel, "Full Name *")
        self.res_name.insert(0, user_data.get("name", ""))

        self.res_email    = labeled_entry(left_panel, "Email Address *")
        self.res_phone    = labeled_entry(left_panel, "Phone Number *")
        self.res_linkedin = labeled_entry(left_panel, "LinkedIn URL (optional)")
        self.res_github   = labeled_entry(left_panel, "GitHub URL (optional)")
        self.res_city     = labeled_entry(left_panel, "City, State / Location *")
        self.res_target   = labeled_entry(left_panel, "Target Job Role (e.g., Software Engineer) *")

        # ---- 3. Education ----
        section_header(left_panel, "\ud83c\udf93", "Education", "#d2a8ff")

        self.edu_container = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.edu_container.pack(fill="x", padx=15)

        def add_education_row(degree="", college="", year="", grade=""):
            rf = ctk.CTkFrame(
                self.edu_container, fg_color="#0d1117",
                corner_radius=8, border_width=1, border_color="#30363d"
            )
            rf.pack(fill="x", pady=4)

            top = ctk.CTkFrame(rf, fg_color="transparent")
            top.pack(fill="x", padx=10, pady=(8, 0))

            deg_e = ctk.CTkEntry(
                top, placeholder_text="Degree / Class / Board",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            deg_e.pack(side="left", fill="x", expand=True, padx=(0, 6))
            if degree:
                deg_e.insert(0, degree)

            yr_e = ctk.CTkEntry(
                top, placeholder_text="Year", width=80,
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            yr_e.pack(side="right")
            if year:
                yr_e.insert(0, year)

            bottom = ctk.CTkFrame(rf, fg_color="transparent")
            bottom.pack(fill="x", padx=10, pady=(4, 8))

            col_e = ctk.CTkEntry(
                bottom, placeholder_text="Institution / School / University",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            col_e.pack(side="left", fill="x", expand=True, padx=(0, 6))
            if college:
                col_e.insert(0, college)

            grade_e = ctk.CTkEntry(
                bottom, placeholder_text="CGPA / %", width=80,
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            grade_e.pack(side="right")
            if grade:
                grade_e.insert(0, grade)

            self.resume_education_rows.append(
                {"degree": deg_e, "college": col_e, "year": yr_e, "grade": grade_e}
            )

        # Pre-fill first row with user's existing college
        add_education_row(college=user_data.get("college", ""))

        ctk.CTkButton(
            left_panel, text="+ Add Education Row",
            fg_color="transparent", border_width=1, border_color="#30363d",
            text_color="#8b949e", hover_color="#21262d", height=32,
            command=add_education_row, font=ctk.CTkFont(size=12)
        ).pack(fill="x", padx=15, pady=5)

        # ---- 4. Experience ----
        section_header(left_panel, "\ud83d\udcbc", "Work / Internship Experience", "#ffa657")

        self.exp_container = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.exp_container.pack(fill="x", padx=15)

        def add_experience_row(role="", company="", duration=""):
            rf = ctk.CTkFrame(
                self.exp_container, fg_color="#0d1117",
                corner_radius=8, border_width=1, border_color="#30363d"
            )
            rf.pack(fill="x", pady=4)

            top = ctk.CTkFrame(rf, fg_color="transparent")
            top.pack(fill="x", padx=10, pady=(8, 0))

            role_e = ctk.CTkEntry(
                top, placeholder_text="Job Title / Role",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            role_e.pack(side="left", fill="x", expand=True, padx=(0, 6))
            if role:
                role_e.insert(0, role)

            dur_e = ctk.CTkEntry(
                top, placeholder_text="Duration", width=110,
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            dur_e.pack(side="right")
            if duration:
                dur_e.insert(0, duration)

            comp_e = ctk.CTkEntry(
                rf, placeholder_text="Company / Organization",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            comp_e.pack(fill="x", padx=10, pady=(4, 8))
            if company:
                comp_e.insert(0, company)

            self.resume_experience_rows.append(
                {"role": role_e, "company": comp_e, "duration": dur_e}
            )

        add_experience_row()

        ctk.CTkButton(
            left_panel, text="+ Add Experience Row",
            fg_color="transparent", border_width=1, border_color="#30363d",
            text_color="#8b949e", hover_color="#21262d", height=32,
            command=add_experience_row, font=ctk.CTkFont(size=12)
        ).pack(fill="x", padx=15, pady=5)

        # ---- 4b. Projects (Optional) ----
        section_header(left_panel, "\ud83d\udcbb", "Projects (Optional)", "#58a6ff")

        self.proj_container = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.proj_container.pack(fill="x", padx=15)

        def add_project_row(title="", desc=""):
            rf = ctk.CTkFrame(
                self.proj_container, fg_color="#0d1117",
                corner_radius=8, border_width=1, border_color="#30363d"
            )
            rf.pack(fill="x", pady=4)

            top = ctk.CTkFrame(rf, fg_color="transparent")
            top.pack(fill="x", padx=10, pady=(8, 0))

            title_e = ctk.CTkEntry(
                top, placeholder_text="Project Title",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            title_e.pack(fill="x", expand=True)
            if title: title_e.insert(0, title)

            bottom = ctk.CTkFrame(rf, fg_color="transparent")
            bottom.pack(fill="x", padx=10, pady=(4, 8))

            desc_e = ctk.CTkEntry(
                bottom, placeholder_text="Project Description",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            desc_e.pack(fill="x", expand=True)
            if desc: desc_e.insert(0, desc)

            self.resume_projects_rows.append({"title": title_e, "desc": desc_e})

        ctk.CTkButton(
            left_panel, text="+ Add Project Row",
            fg_color="transparent", border_width=1, border_color="#30363d",
            text_color="#8b949e", hover_color="#21262d", height=32,
            command=add_project_row, font=ctk.CTkFont(size=12)
        ).pack(fill="x", padx=15, pady=5)

        # ---- 4c. Certifications (Optional) ----
        section_header(left_panel, "\ud83c\udfc6", "Achievements / Certifications (Optional)", "#d2a8ff")

        self.cert_container = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.cert_container.pack(fill="x", padx=15)

        def add_cert_row(title="", desc=""):
            rf = ctk.CTkFrame(
                self.cert_container, fg_color="#0d1117",
                corner_radius=8, border_width=1, border_color="#30363d"
            )
            rf.pack(fill="x", pady=4)

            top = ctk.CTkFrame(rf, fg_color="transparent")
            top.pack(fill="x", padx=10, pady=(8, 8))

            title_e = ctk.CTkEntry(
                top, placeholder_text="Certification / Achievement",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            title_e.pack(side="left", fill="x", expand=True, padx=(0, 6))
            if title: title_e.insert(0, title)
            
            desc_e = ctk.CTkEntry(
                top, placeholder_text="Details / Issuer",
                height=34, fg_color="#161b22", border_color="#30363d",
                font=ctk.CTkFont(size=12)
            )
            desc_e.pack(side="left", fill="x", expand=True)
            if desc: desc_e.insert(0, desc)

            self.resume_certs_rows.append({"title": title_e, "desc": desc_e})

        ctk.CTkButton(
            left_panel, text="+ Add Certification Row",
            fg_color="transparent", border_width=1, border_color="#30363d",
            text_color="#8b949e", hover_color="#21262d", height=32,
            command=add_cert_row, font=ctk.CTkFont(size=12)
        ).pack(fill="x", padx=15, pady=5)

        # ---- 5. Skills ----
        section_header(left_panel, "\ud83d\udee0\ufe0f", "Skills", "#79c0ff")

        skill_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        skill_row.pack(fill="x", padx=15, pady=4)

        self.skill_entry = ctk.CTkEntry(
            skill_row, placeholder_text="Type a skill and press Add or Enter",
            height=38, fg_color="#0d1117", border_color="#30363d",
            font=ctk.CTkFont(size=13)
        )
        self.skill_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.skill_tags_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.skill_tags_frame.pack(fill="x", padx=15, pady=4)

        def add_skill_tag(event=None):
            skill_text = self.skill_entry.get().strip()
            if not skill_text or skill_text in self.resume_skills_list:
                return
            self.resume_skills_list.append(skill_text)
            tag = ctk.CTkFrame(
                self.skill_tags_frame, fg_color="#1f3a6e", corner_radius=14,
                border_width=1, border_color="#388bfd"
            )
            tag.pack(side="left", padx=4, pady=3)
            lbl = ctk.CTkLabel(
                tag, text=f"  {skill_text}  \u2715",
                font=ctk.CTkFont(size=12), text_color="#79c0ff"
            )
            lbl.pack(padx=4, pady=5)

            def remove_tag(e, t=tag, s=skill_text):
                if s in self.resume_skills_list:
                    self.resume_skills_list.remove(s)
                t.destroy()

            tag.bind("<Button-1>", remove_tag)
            lbl.bind("<Button-1>", remove_tag)
            self.skill_entry.delete(0, "end")

        ctk.CTkButton(
            skill_row, text="Add", width=72, height=38,
            fg_color="#2ea043", hover_color="#3fb950",
            command=add_skill_tag, font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="right")
        self.skill_entry.bind("<Return>", add_skill_tag)

        # Pre-populate a few sensible defaults
        for sk_default in ["Communication", "Problem Solving", "Teamwork"]:
            self.skill_entry.delete(0, "end")
            self.skill_entry.insert(0, sk_default)
            add_skill_tag()

        # ======== RIGHT PANEL – PREVIEW ========
        right_panel = ctk.CTkFrame(
            body, fg_color="#161b22", corner_radius=12,
            border_width=1, border_color="#30363d"
        )
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 20), pady=10)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Right panel header
        rp_head = ctk.CTkFrame(right_panel, fg_color="#1c2128", corner_radius=10)
        rp_head.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        rp_inner = ctk.CTkFrame(rp_head, fg_color="transparent")
        rp_inner.pack(fill="x", padx=20, pady=14)
        ctk.CTkLabel(
            rp_inner, text="\ud83d\udc41  Resume Preview",
            font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
            text_color="#f0f6fc"
        ).pack(side="left")
        ctk.CTkLabel(
            rp_inner,
            text="AI-generated content will appear here after you click Generate",
            text_color="#8b949e", font=ctk.CTkFont(size=12)
        ).pack(side="right")

        # Scrollable preview area
        self.resume_preview_scroll = ctk.CTkScrollableFrame(
            right_panel, fg_color="#0d1117", corner_radius=10,
            scrollbar_button_color="#21262d",
            scrollbar_button_hover_color="#30363d"
        )
        self.resume_preview_scroll.grid(
            row=1, column=0, sticky="nsew", padx=15, pady=(8, 5)
        )

        # Placeholder text
        ctk.CTkLabel(
            self.resume_preview_scroll,
            text=(
                "\u2728  Fill in the form on the left, then click\n"
                "\"Generate with AI\" to build your resume preview."
            ),
            text_color="#30363d",
            font=ctk.CTkFont(family="Inter", size=15),
            justify="center"
        ).pack(pady=100)

        # Action buttons
        btn_bar = ctk.CTkFrame(right_panel, fg_color="transparent")
        btn_bar.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 15))

        self.resume_gen_btn = ctk.CTkButton(
            btn_bar,
            text="\ud83e\udd16  Generate with AI",
            height=48, fg_color="#8957e5", hover_color="#9f75ec",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.resume_trigger_ai
        )
        self.resume_gen_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.resume_export_btn = ctk.CTkButton(
            btn_bar,
            text="\ud83d\udce5  Export PDF",
            height=48, fg_color="#238636", hover_color="#2ea043",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.resume_export_pdf
        )
        self.resume_export_btn.pack(side="right", fill="x", expand=True, padx=(8, 0))

    def resume_trigger_ai(self):
        """Collect form data, validate, then call Gemini AI in a background thread."""
        name        = self.res_name.get().strip()
        email       = self.res_email.get().strip()
        phone       = self.res_phone.get().strip()
        linkedin    = self.res_linkedin.get().strip()
        city        = self.res_city.get().strip()
        target_role = self.res_target.get().strip()

        if not name or not target_role:
            messagebox.showerror(
                "Missing Fields",
                "Please fill in at least your Full Name and Target Job Role before generating."
            )
            return

        # Collect education
        education_lines = []
        for row in self.resume_education_rows:
            deg = row["degree"].get().strip()
            col = row["college"].get().strip()
            yr  = row["year"].get().strip()
            grd = row["grade"].get().strip()
            if deg or col:
                line = f"{deg} from {col} ({yr})"
                if grd:
                    line += f" - Score: {grd}"
                education_lines.append(line)

        # Collect experience
        experience_lines = []
        for row in self.resume_experience_rows:
            role = row["role"].get().strip()
            comp = row["company"].get().strip()
            dur  = row["duration"].get().strip()
            if role or comp:
                experience_lines.append(f"{role} at {comp} ({dur})")

        github = getattr(self, "res_github", None)
        github_val = github.get().strip() if github else ""

        # Collect projects
        proj_lines = []
        for row in getattr(self, "resume_projects_rows", []):
            t = row["title"].get().strip()
            d = row["desc"].get().strip()
            if t or d: proj_lines.append(f"{t}: {d}")

        # Collect certs
        cert_lines = []
        for row in getattr(self, "resume_certs_rows", []):
            t = row["title"].get().strip()
            d = row["desc"].get().strip()
            if t or d: cert_lines.append(f"{t}: {d}")

        data = {
            "name":        name,
            "email":       email,
            "phone":       phone,
            "linkedin":    linkedin,
            "github":      github_val,
            "location":    city,
            "target_role": target_role,
            "education":   "; ".join(education_lines) if education_lines else "Details not provided",
            "experience":  "; ".join(experience_lines) if experience_lines else "Fresher / No prior experience",
            "skills":      ", ".join(self.resume_skills_list) if self.resume_skills_list else "General professional skills",
            "projects":    "; ".join(proj_lines) if proj_lines else "",
            "certs":       "; ".join(cert_lines) if cert_lines else "",
        }
        self._resume_data_cache = data

        # Show loading state
        self.resume_gen_btn.configure(state="disabled", text="\u23f3  Generating...")
        for widget in self.resume_preview_scroll.winfo_children():
            widget.destroy()

        loading_lbl = ctk.CTkLabel(
            self.resume_preview_scroll,
            text="\ud83e\udd16  Gemini AI is crafting your resume\u2026",
            text_color="#8957e5", font=ctk.CTkFont(size=15)
        )
        loading_lbl.pack(pady=30)
        prog = ctk.CTkProgressBar(
            self.resume_preview_scroll, width=300,
            progress_color="#8957e5", mode="indeterminate"
        )
        prog.pack(pady=10)
        prog.start()

        def run_in_thread():
            from ai_service import generate_resume_content
            ai_result = generate_resume_content(data)
            self.resume_ai_content = ai_result
            self.after(0, lambda: self.resume_render_preview(data, ai_result))

        threading.Thread(target=run_in_thread, daemon=True).start()

    def resume_render_preview(self, data, ai):
        """Render the styled resume preview in the right panel."""
        self.resume_gen_btn.configure(state="normal", text="\ud83e\udd16  Generate with AI")

        for widget in self.resume_preview_scroll.winfo_children():
            widget.destroy()

        PX = 20  # horizontal padding shorthand

        # ---- Header block (blue) ----
        hdr = ctk.CTkFrame(
            self.resume_preview_scroll, fg_color="#1f6feb", corner_radius=10
        )
        hdr.pack(fill="x", padx=PX, pady=(10, 5))

        hdr_inner = ctk.CTkFrame(hdr, fg_color="transparent")
        hdr_inner.pack(fill="x", padx=20, pady=15)

        # Photo thumbnail in preview (top-right)
        if self.resume_photo_path:
            try:
                img = Image.open(self.resume_photo_path).resize((72, 72))
                ctk_img = ctk.CTkImage(img, size=(72, 72))
                photo_lbl = ctk.CTkLabel(hdr_inner, image=ctk_img, text="")
                photo_lbl._image = ctk_img
                photo_lbl.pack(side="right", padx=(10, 0))
            except Exception:
                pass

        ctk.CTkLabel(
            hdr_inner, text=data["name"].upper(),
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        ctk.CTkLabel(
            hdr_inner, text=data["target_role"],
            font=ctk.CTkFont(size=14), text_color="#c9d1d9"
        ).pack(anchor="w")
        contact_parts = [
            p for p in [data.get("email"), data.get("phone"), data.get("location")]
            if p
        ]
        if contact_parts:
            ctk.CTkLabel(
                hdr_inner, text="  \u2022  ".join(contact_parts),
                font=ctk.CTkFont(size=11), text_color="#adbac7"
            ).pack(anchor="w", pady=(4, 0))
        if data.get("linkedin"):
            ctk.CTkLabel(
                hdr_inner, text=data["linkedin"],
                font=ctk.CTkFont(size=11), text_color="#79c0ff"
            ).pack(anchor="w")

        # ---- Helper: section block in preview ----
        def preview_section(title, content, accent="#58a6ff"):
            sec = ctk.CTkFrame(
                self.resume_preview_scroll, fg_color="#161b22",
                corner_radius=8, border_width=1, border_color="#30363d"
            )
            sec.pack(fill="x", padx=PX, pady=5)
            ctk.CTkLabel(
                sec, text=title,
                font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                text_color=accent
            ).pack(anchor="w", padx=15, pady=(12, 3))
            ctk.CTkFrame(sec, height=1, fg_color="#30363d").pack(fill="x", padx=15)
            ctk.CTkLabel(
                sec, text=content, text_color="#c9d1d9",
                wraplength=480, justify="left",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", padx=15, pady=(7, 12))

        # ---- AI-generated sections ----
        preview_section(
            "\ud83c\udfaf  Career Objective",
            ai.get("objective", "N/A"),
            "#58a6ff"
        )
        preview_section(
            "\ud83d\udccb  Professional Summary",
            ai.get("summary", "N/A"),
            "#2ea043"
        )

        # Key Strengths (bullet list)
        strengths = ai.get("strengths", [])
        if strengths:
            ssec = ctk.CTkFrame(
                self.resume_preview_scroll, fg_color="#161b22",
                corner_radius=8, border_width=1, border_color="#30363d"
            )
            ssec.pack(fill="x", padx=PX, pady=5)
            ctk.CTkLabel(
                ssec, text="\u26a1  Key Strengths",
                font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                text_color="#d2a8ff"
            ).pack(anchor="w", padx=15, pady=(12, 3))
            ctk.CTkFrame(ssec, height=1, fg_color="#30363d").pack(fill="x", padx=15)
            for s in strengths:
                ctk.CTkLabel(
                    ssec, text=f"   \u2726  {s}",
                    text_color="#c9d1d9", font=ctk.CTkFont(size=12), anchor="w"
                ).pack(anchor="w", padx=15, pady=3)
            ctk.CTkFrame(ssec, height=8, fg_color="transparent").pack()

        # ---- Form-sourced sections ----
        edu_lines = []
        for r in self.resume_education_rows:
            deg = r['degree'].get().strip()
            col = r['college'].get().strip()
            yr  = r['year'].get().strip()
            grd = r['grade'].get().strip()
            if deg or col:
                line = f"\u2022  {deg} \u2014 {col}"
                if yr: line += f" ({yr})"
                if grd: line += f"  |  Score: {grd}"
                edu_lines.append(line)

        if edu_lines:
            preview_section("\ud83c\udf93  Education", "\n".join(edu_lines), "#d2a8ff")

        exp_lines = [
            f"\u2022  {r['role'].get()} at {r['company'].get()} \u2014 {r['duration'].get()}"
            for r in self.resume_experience_rows
            if r["role"].get().strip() or r["company"].get().strip()
        ]
        if exp_lines:
            preview_section(
                "\ud83d\udcbc  Work / Internship Experience",
                "\n".join(exp_lines), "#ffa657"
            )

        if self.resume_skills_list:
            preview_section(
                "\ud83d\udee0\ufe0f  Skills",
                "  \u2022  ".join(self.resume_skills_list),
                "#79c0ff"
            )

        proj_lines = [
            f"\u2022  {r['title'].get()} \u2014 {r['desc'].get()}"
            for r in getattr(self, "resume_projects_rows", [])
            if r["title"].get().strip() or r["desc"].get().strip()
        ]
        if proj_lines:
            preview_section("\ud83d\udcbb  Projects", "\n".join(proj_lines), "#58a6ff")

        cert_lines = [
            f"\u2022  {r['title'].get()} \u2014 {r['desc'].get()}"
            for r in getattr(self, "resume_certs_rows", [])
            if r["title"].get().strip() or r["desc"].get().strip()
        ]
        if cert_lines:
            preview_section("\ud83c\udfc6  Certifications", "\n".join(cert_lines), "#d2a8ff")

    def resume_export_pdf(self):
        """Export a clean, minimalist, traditional format resume PDF using fpdf2."""
        if not self._resume_data_cache:
            messagebox.showwarning("Not Ready", "Please generate your resume with AI first, then export.")
            return

        data = self._resume_data_cache
        ai   = self.resume_ai_content
        import os

        filename = f"{self.current_user}_resume.pdf"

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_margins(15, 15, 15)
            pdf.set_text_color(0, 0, 0)

            # ---- HEADER ----
            # Determine if photo is present so we can adjust text width
            PHOTO_W    = 32   # mm wide
            PHOTO_H    = 38   # mm tall
            PHOTO_X    = 178  # mm from left (right margin area)
            PHOTO_Y    = 10   # mm from top
            TEXT_W     = 150  # safe width that won't overlap photo
            has_photo  = bool(self.resume_photo_path and os.path.exists(self.resume_photo_path))

            # Place photo first (behind text in Z order)
            if has_photo:
                try:
                    tmp_photo = f"{self.current_user}_tmp_photo.jpg"
                    img = Image.open(self.resume_photo_path)
                    # Crop to square from center for clean photo
                    w, h = img.size
                    side = min(w, h)
                    left = (w - side) // 2
                    top  = (h - side) // 2
                    img = img.crop((left, top, left + side, top + side)).resize((200, 200))
                    img.save(tmp_photo)
                    pdf.image(tmp_photo, x=PHOTO_X, y=PHOTO_Y, w=PHOTO_W, h=PHOTO_H)
                    if os.path.exists(tmp_photo):
                        os.remove(tmp_photo)
                except Exception:
                    has_photo = False

            # Name (large bold)
            pdf.set_font("Helvetica", "B", 22)
            name_safe = data.get("name", "Name").encode("latin-1", "replace").decode("latin-1")
            pdf.set_xy(15, 12)
            pdf.cell(TEXT_W, 10, name_safe, new_x="LMARGIN", new_y="NEXT")

            # Target role (subtitle)
            if data.get("target_role"):
                pdf.set_font("Helvetica", "I", 12)
                role_safe = data["target_role"].encode("latin-1", "replace").decode("latin-1")
                pdf.set_x(15)
                pdf.cell(TEXT_W, 6, role_safe, new_x="LMARGIN", new_y="NEXT")

            # Contact line 1 — Email | Phone | Location
            # Using latin-1 safe bracket-icon style: [E] [M] [Loc]
            pdf.set_font("Helvetica", "", 9)
            contact_parts = []
            if data.get("email"):
                contact_parts.append("[E] " + data["email"])
            if data.get("phone"):
                contact_parts.append("[M] " + data["phone"])
            if data.get("location"):
                contact_parts.append("[Loc] " + data["location"])

            if contact_parts:
                contact_str = "   |   ".join(contact_parts)
                contact_str = contact_str.encode("latin-1", "replace").decode("latin-1")
                pdf.set_x(15)
                pdf.cell(TEXT_W, 6, contact_str, new_x="LMARGIN", new_y="NEXT")

            # Contact line 2 — GitHub | LinkedIn
            links = []
            if data.get("github"):
                links.append("[GitHub] " + data["github"])
            if data.get("linkedin"):
                links.append("[LinkedIn] " + data["linkedin"])
            if links:
                links_str = "   |   ".join(links).encode("latin-1", "replace").decode("latin-1")
                pdf.set_x(15)
                pdf.cell(TEXT_W, 6, links_str, new_x="LMARGIN", new_y="NEXT")

            # Horizontal divider — drawn BELOW whichever is taller: text block or photo
            text_bottom = pdf.get_y() + 4
            photo_bottom = PHOTO_Y + PHOTO_H + 4 if has_photo else 0
            divider_y = max(text_bottom, photo_bottom)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(0.8)
            pdf.line(15, divider_y, 195, divider_y)
            pdf.set_line_width(0.2)
            pdf.set_y(divider_y + 5)


            # ---- Helper: Solid Section Line ----
            def render_section_title(title):
                pdf.set_font("Helvetica", "B", 13)
                pdf.set_text_color(0, 0, 0)
                clean_t = title.upper().encode("latin-1", "replace").decode("latin-1")
                pdf.cell(0, 8, clean_t, new_x="LMARGIN", new_y="NEXT")
                
                # Draw thick black horizontal line under title
                x, y = pdf.get_x(), pdf.get_y()
                pdf.set_line_width(0.7)
                pdf.line(x, y, 200, y)
                pdf.set_line_width(0.2) # reset
                pdf.ln(3)

            # ---- AI SUMMARY & STRENGTHS ----
            if ai.get("objective") or ai.get("summary"):
                render_section_title("Summary")
                pdf.set_font("Helvetica", "", 11)
                t = (ai.get("summary") or ai.get("objective")).encode("latin-1", "replace").decode("latin-1")
                pdf.multi_cell(0, 5, t, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)
                
            # ---- EDUCATION ----
            if self.resume_education_rows:
                has_edu = any(r["degree"].get().strip() or r["college"].get().strip() for r in self.resume_education_rows)
                if has_edu:
                    render_section_title("Education")
                    for r in self.resume_education_rows:
                        deg = r["degree"].get().strip().encode("latin-1", "replace").decode("latin-1")
                        col = r["college"].get().strip().encode("latin-1", "replace").decode("latin-1")
                        yr  = r["year"].get().strip().encode("latin-1", "replace").decode("latin-1")
                        grd = r["grade"].get().strip().encode("latin-1", "replace").decode("latin-1")
                        
                        if not deg and not col: continue
                        
                        # Line 1: Degree (Bold, Left) | Year (Normal, Right)
                        pdf.set_font("Helvetica", "B", 11)
                        pdf.cell(150, 6, deg)
                        pdf.set_font("Helvetica", "", 10)
                        pdf.cell(0, 6, yr, align="R", new_x="LMARGIN", new_y="NEXT")
                        
                        # Line 2: College (Italic)
                        if col:
                            pdf.set_font("Helvetica", "I", 10)
                            pdf.cell(0, 5, col, new_x="LMARGIN", new_y="NEXT")
                        
                        # Line 3: Grade
                        if grd:
                            pdf.set_font("Helvetica", "", 10)
                            pdf.cell(0, 5, f"CGPA/Percentage: {grd}", new_x="LMARGIN", new_y="NEXT")
                        pdf.ln(3)

            # ---- SKILLS ----
            if self.resume_skills_list:
                render_section_title("Technical Skills")
                pdf.set_font("Helvetica", "", 11)
                skills_str = ", ".join(self.resume_skills_list).encode("latin-1", "replace").decode("latin-1")
                pdf.multi_cell(0, 6, skills_str, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)

            # ---- PROJECTS (Conditional) ----
            proj_rows = getattr(self, "resume_projects_rows", [])
            has_projects = any(r["title"].get().strip() or r["desc"].get().strip() for r in proj_rows)
            if has_projects:
                render_section_title("Projects")
                for r in proj_rows:
                    t = r["title"].get().strip().encode("latin-1", "replace").decode("latin-1")
                    d = r["desc"].get().strip().encode("latin-1", "replace").decode("latin-1")
                    if not t and not d: continue
                    
                    pdf.set_font("Helvetica", "B", 11)
                    if t:
                        pdf.cell(0, 6, t, new_x="LMARGIN", new_y="NEXT")
                    pdf.set_font("Helvetica", "", 10)
                    if d:
                        pdf.multi_cell(0, 5, "  * " + d, new_x="LMARGIN", new_y="NEXT")
                    pdf.ln(3)

            # ---- EXPERIENCE ----
            if self.resume_experience_rows:
                has_exp = any(r["role"].get().strip() or r["company"].get().strip() for r in self.resume_experience_rows)
                if has_exp:
                    render_section_title("Experience")
                    for r in self.resume_experience_rows:
                        role = r["role"].get().strip().encode("latin-1", "replace").decode("latin-1")
                        comp = r["company"].get().strip().encode("latin-1", "replace").decode("latin-1")
                        dur  = r["duration"].get().strip().encode("latin-1", "replace").decode("latin-1")
                        
                        if not role and not comp: continue
                        
                        pdf.set_font("Helvetica", "B", 11)
                        if role:
                            pdf.cell(150, 6, role)
                        else:
                            pdf.cell(150, 6, "")
                        
                        pdf.set_font("Helvetica", "", 10)
                        pdf.cell(0, 6, dur, align="R", new_x="LMARGIN", new_y="NEXT")
                        
                        if comp:
                            pdf.set_font("Helvetica", "I", 10)
                            pdf.cell(0, 5, comp, new_x="LMARGIN", new_y="NEXT")
                        pdf.ln(3)

            # ---- CERTIFICATIONS ----
            cert_rows = getattr(self, "resume_certs_rows", [])
            has_certs = any(r["title"].get().strip() or r["desc"].get().strip() for r in cert_rows)
            if has_certs:
                render_section_title("Achievements & Certifications")
                for r in cert_rows:
                    t = r["title"].get().strip().encode("latin-1", "replace").decode("latin-1")
                    d = r["desc"].get().strip().encode("latin-1", "replace").decode("latin-1")
                    if not t and not d: continue
                    
                    pdf.set_font("Helvetica", "B", 11)
                    if t:
                        pdf.cell(0, 6, t, new_x="LMARGIN", new_y="NEXT")
                    pdf.set_font("Helvetica", "", 10)
                    if d:
                        pdf.multi_cell(0, 5, d, new_x="LMARGIN", new_y="NEXT")
                    pdf.ln(3)

            pdf.output(filename)
            messagebox.showinfo("Resume Exported \u2713", f"Your resume has been saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not generate resume PDF:\n{e}")


if __name__ == "__main__":
    app = AdvancedCareerApp()
    app.mainloop()
