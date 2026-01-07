import os
import pickle
import numpy as np
from feature_extraction import extract_features

MODEL_PATH = "models/tamper_model.pkl"

def detect_tampering(file_path: str):
    if not os.path.exists(MODEL_PATH):
        return "Error: Model file not found. Run train.py first."

    with open(MODEL_PATH, "rb") as f:
        data = pickle.load(f)
        model = data['model']
        scaler = data['scaler']

    features = extract_features(file_path)
    features_array = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features_array)

    prediction = model.predict(features_scaled)[0]

    if prediction == 0:
        return "✅ File is SAFE (Not Tampered)"
    else:
        return "❌ File is TAMPERED"

if __name__ == "__main__":
    test_file = "data/tampered/"
    
    if os.path.exists(test_file):
        print(f"Analyzing: {test_file}")
        print(detect_tampering(test_file))
    else:
        print(f"Test file not found: {test_file}")