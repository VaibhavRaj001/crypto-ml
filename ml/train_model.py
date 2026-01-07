import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from feature_extraction import extract_features

ORIGINAL_DIR = "data/original"
TAMPERED_DIR = "data/tampered"
MODEL_PATH = "models/tamper_model.pkl"


def load_dataset():
    X, y = [], []

    for file in os.listdir(ORIGINAL_DIR):
        path = os.path.join(ORIGINAL_DIR, file)
        X.append(extract_features(path))
        y.append(0)  # original

    for file in os.listdir(TAMPERED_DIR):
        path = os.path.join(TAMPERED_DIR, file)
        X.append(extract_features(path))
        y.append(1)  # tampered

    return X, y


def train():
    X, y = load_dataset()

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("✅ Model trained and saved successfully!")


if __name__ == "__main__":
    train()
