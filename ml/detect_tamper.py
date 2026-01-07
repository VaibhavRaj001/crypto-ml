import pickle
from feature_extraction import extract_features

MODEL_PATH = "models/tamper_model.pkl"


def detect_tampering(file_path: str):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    features = extract_features(file_path)
    prediction = model.predict([features])[0]

    if prediction == 0:
        return "File is SAFE (Not Tampered)"
    else:
        return "File is TAMPERED"


if __name__ == "__main__":
    test_file = "decrypted_files/Copy of ROOKUS_PITCH_20251212_002416_0000.pdf"
    print(detect_tampering(test_file))
