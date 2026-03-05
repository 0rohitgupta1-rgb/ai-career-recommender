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

# Initialize ML Predictor (this will train or load the model)
ml_engine = MLPredictor()

# Setup themes
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# The 12 features we train on
FEATURES = [
    "Mathematics", "Science", "English", "Aptitude Space", 
    "Technical Knack", "Communication", "Logical Reasoning", 
    "Creative Ability", "Arts Interest", "Science Interest", 
    "Commercial Awareness", "Big 5: Extroversion"
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
        
        self.show_login_screen()

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
        self.sidebar.grid_rowconfigure(5, weight=1) # Push logout to bottom
        
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
        
        # Bottom controls
        self.nav_logout = ctk.CTkButton(self.sidebar, text="Sign Out", fg_color="#da3633", hover_color="#f85149", anchor="center", font=ctk.CTkFont(size=14, weight="bold"), height=40, command=self.show_login_screen)
        self.nav_logout.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        
        # 2. Main Content Frame
        self.main_content = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")

    def reset_sidebar(self):
        for btn in [self.nav_home, self.nav_assess, self.nav_history]:
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
        ctk.CTkLabel(banner, text="Take the 12-factor aptitude and skill assessment to get AI-powered recommendations.", font=ctk.CTkFont(size=15), text_color="#c9d1d9").place(relx=0.1, rely=0.5, anchor="w")
        
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
        ctk.CTkLabel(header, text="Adjust the 12 parameters to your perceived skill levels.", text_color="#8b949e", font=ctk.CTkFont(size=14)).pack(side="left", padx=20, pady=10)

        # Main Scrollable Form
        form_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="#161b22", corner_radius=15, border_width=1, border_color="#30363d")
        form_frame.pack(fill="both", expand=True, padx=40, pady=(10, 30))
        
        self.sliders = []
        
        # Categorize the 12 features for better UI
        categories = {
            "Core Cognitive": (FEATURES[0:4], "#1f6aa5"),
            "Technical & Expression": (FEATURES[4:8], "#2ea043"),
            "Applied & Extroversion": (FEATURES[8:12], "#9e6a03")
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
        
        # 1. Run ML Predictor
        ml_results = ml_engine.predict(scores)
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
            # Fallback to viridis if list length mismatch, but list is 12 long
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

if __name__ == "__main__":
    app = AdvancedCareerApp()
    app.mainloop()