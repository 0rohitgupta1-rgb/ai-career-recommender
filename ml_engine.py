import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

# 30 Distinct Career Paths
CAREER_PROFILES = {
    # Tech & Software
    "Software Engineer": { "high": [0, 3, 4, 6], "low": [8, 11] },
    "Data Scientist": { "high": [0, 1, 3, 4, 6, 9], "low": [7, 8] },
    "Cloud Architect": { "high": [3, 4, 6, 10], "low": [8] },
    "Cybersecurity Analyst": { "high": [3, 4, 6], "low": [8, 11] },
    "DevOps Engineer": { "high": [4, 6, 10], "low": [8] },
    "Game Developer": { "high": [0, 4, 6, 7], "low": [11] },
    "Blockchain Developer": { "high": [0, 3, 4, 6, 10], "low": [8] },
    "AI/ML Engineer": { "high": [0, 1, 3, 4, 6, 9], "low": [8] },
    "Mobile App Developer": { "high": [4, 6, 7], "low": [] },
    "Database Administrator": { "high": [3, 4, 6], "low": [7, 8] },
    "IT Support Specialist": { "high": [4, 5, 11], "low": [0, 1] },
    "Network Engineer": { "high": [3, 4, 6], "low": [7, 8] },
    "Hardware Engineer": { "high": [0, 1, 4, 6, 9], "low": [8] },

    # Design & Creative
    "UI/UX Designer": { "high": [4, 5, 7, 8], "low": [0, 1, 9] },
    "Graphic Designer": { "high": [7, 8], "low": [0, 1, 9] },
    "Video Editor": { "high": [4, 7, 8], "low": [0, 1, 9] },
    "Content Creator": { "high": [2, 5, 7, 8, 11], "low": [0, 1, 9] },

    # Business, Mgmt & Marketing
    "Product Manager": { "high": [3, 4, 5, 6, 10, 11], "low": [8] },
    "Digital Marketer": { "high": [2, 5, 7, 10, 11], "low": [1, 9] },
    "Sales Manager": { "high": [5, 10, 11], "low": [1, 9] },
    "HR Specialist": { "high": [2, 5, 11], "low": [0, 1, 4, 9] },
    "Financial Analyst": { "high": [0, 3, 6, 10], "low": [7, 8] },
    "Technical Writer": { "high": [2, 4, 5, 6], "low": [8, 11] },
    "SEO Specialist": { "high": [2, 3, 4, 6, 10], "low": [8] },
    "Public Relations Manager": { "high": [2, 5, 10, 11], "low": [0, 1, 9] },
    "Event Planner": { "high": [5, 7, 10, 11], "low": [0, 1, 9] },

    # Traditional Engineering
    "Mechanical Engineer": { "high": [0, 1, 3, 6, 9], "low": [8] },
    "Biomedical Engineer": { "high": [0, 1, 3, 6, 9], "low": [8] },
    "Civil Engineer": { "high": [0, 1, 3, 6, 9], "low": [8] },
    "Electrical Engineer": { "high": [0, 1, 3, 6, 9], "low": [8] }
}

def generate_synthetic_data(num_samples_per_career=200):
    """Generates synthetic student profiles for training the model balancing all 30 careers."""
    np.random.seed(42)
    X = []
    y = []

    careers = list(CAREER_PROFILES.keys())

    for career in careers:
        profile_req = CAREER_PROFILES[career]
        high_traits = profile_req["high"]
        low_traits = profile_req["low"]

        for _ in range(num_samples_per_career):
            # Base randomized profile (average student) 40 to 70 range
            profile = np.random.randint(40, 71, size=12)

            # Boost high traits strongly (75 to 100)
            for ht in high_traits:
                profile[ht] = np.random.randint(75, 101)

            # Suppress low traits (10 to 45)
            for lt in low_traits:
                profile[lt] = np.random.randint(10, 46)

            # Add minor noise
            profile = profile + np.random.randint(-5, 6, size=12)
            profile = np.clip(profile, 0, 100)

            X.append(profile)
            y.append(career)

    return np.array(X), np.array(y)

def train_and_save_model(model_path="career_model.pkl", scaler_path="scaler.pkl"):
    print("Generating highly distinct synthetic dataset for 30 careers...")
    X, y = generate_synthetic_data(num_samples_per_career=200) # 6000 total samples
    
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("Training RandomForest model...")
    # Using more estimators and depth for 30 distinct classes
    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=15, min_samples_split=5)
    model.fit(X_scaled, y)
    
    accuracy = model.score(X_scaled, y)
    print(f"Model trained with synthetic accuracy: {accuracy:.4f}")
    
    print(f"Saving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Saving scaler to {scaler_path}...")
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
        
    return model, scaler

class MLPredictor:
    def __init__(self, model_path="career_model.pkl", scaler_path="scaler.pkl"):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self._load_or_train()
        
    def _load_or_train(self):
        # Force retrain if we are updating the model to 30 classes 
        # (This ensures old pkl files don't interfere)
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            # Simple check if model has 30 classes
            if len(self.model.classes_) < 30:
                print("Old model detected. Retraining...")
                self.model, self.scaler = train_and_save_model(self.model_path, self.scaler_path)
            else:
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
        except Exception as e:
            print("Retraining model...")
            self.model, self.scaler = train_and_save_model(self.model_path, self.scaler_path)
            
    def predict(self, features):
        """Predicts the career and returns the top 3 recommendations."""
        if len(features) < 12:
            features = list(features) + [50] * (12 - len(features))
        features = np.array(features[:12]).reshape(1, -1)
        
        scaled_features = self.scaler.transform(features)
        
        probs = self.model.predict_proba(scaled_features)[0]
        top_3_idx = np.argsort(probs)[::-1][:3]
        
        classes = self.model.classes_
        recommendations = [(classes[i], probs[i]) for i in top_3_idx]
        
        return recommendations

if __name__ == "__main__":
    train_and_save_model()
