import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from feature_extraction import extract_features

ORIGINAL_DIR = "data/original"
TAMPERED_DIR = "data/tampered"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "tamper_model.pkl")

def load_dataset():
    """Loads files from folders and extracts features."""
    X, y = [], []

    if os.path.exists(ORIGINAL_DIR):
        print(f"Reading original files from {ORIGINAL_DIR}...")
        for file in os.listdir(ORIGINAL_DIR):
            path = os.path.join(ORIGINAL_DIR, file)
            if os.path.isfile(path):
                features = extract_features(path)
                X.append(features)
                y.append(0)
    else:
        print(f"Error: {ORIGINAL_DIR} not found.")

    if os.path.exists(TAMPERED_DIR):
        print(f"Reading tampered files from {TAMPERED_DIR}...")
        for file in os.listdir(TAMPERED_DIR):
            path = os.path.join(TAMPERED_DIR, file)
            if os.path.isfile(path):
                features = extract_features(path)
                X.append(features)
                y.append(1)
    else:
        print(f"Error: {TAMPERED_DIR} not found.")

    return np.array(X), np.array(y)

def train_model():
    X, y = load_dataset()

    if len(X) == 0:
        print("❌ Training failed: No data found in directories.")
        return

    print(f"Dataset loaded: {len(X)} samples found.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100, 
        max_depth=10,     
        random_state=42
    )
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print("\n--- Model Performance Report ---")
    print(classification_report(y_test, y_pred, target_names=["Safe", "Tampered"]))
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump({
            'model': model, 
            'scaler': scaler,
            'features_list': ['size', 'entropy', 'mean', 'std', 'is_pdf', 'is_jpg']
        }, f)

    print(f"\n✅ Model and Scaler saved successfully to {MODEL_PATH}!")

if __name__ == "__main__":
    train_model()