"""
Passive Attack Detection using Machine Learning
Detects eavesdropping, timing attacks, cache attacks, and other passive threats
"""
import os
import json
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

PASSIVE_DATA_DIR = "data/passive_attacks"
MODEL_DIR = "models"
PASSIVE_MODEL_PATH = os.path.join(MODEL_DIR, "passive_attack_model.pkl")

# Feature names for the 8 behavioral vectors
FEATURE_NAMES = [
    'read_ops_per_sec',
    'avg_read_block_size',
    'session_duration',
    'decrypt_calls',
    'entropy_of_read_sequence',
    'cache_miss_rate',
    'reopen_frequency',
    'access_time_zscore'
]


def load_passive_dataset(filename):
    """Load passive attack dataset from JSON"""
    filepath = os.path.join(PASSIVE_DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ Error: {filepath} not found")
        return None, None
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    X = []
    y = []
    
    for record in data:
        features = [record[feat] for feat in FEATURE_NAMES]
        X.append(features)
        y.append(record['label'])
    
    return np.array(X), np.array(y)


def train_passive_detector():
    """Train machine learning model for passive attack detection"""
    print("=" * 60)
    print("PASSIVE ATTACK DETECTION - MODEL TRAINING")
    print("=" * 60)
    
    # Load training data
    X_train, y_train = load_passive_dataset('passive_train.json')
    
    if X_train is None:
        print("❌ Training failed: Dataset not found. Run passive_data_generator.py first.")
        return
    
    print(f"\n📊 Training dataset loaded: {len(X_train)} samples")
    print(f"   Normal behavior: {np.sum(y_train == 0)}")
    print(f"   Passive attacks: {np.sum(y_train == 1)}")
    
    # Split for validation
    X_train_split, X_val, y_train_split, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_split)
    X_val_scaled = scaler.transform(X_val)
    
    # Train Gradient Boosting Classifier (better for behavioral patterns)
    print("\n🔧 Training Gradient Boosting Classifier...")
    model = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        subsample=0.8
    )
    
    model.fit(X_train_scaled, y_train_split)
    
    # Validation
    y_pred = model.predict(X_val_scaled)
    y_pred_proba = model.predict_proba(X_val_scaled)[:, 1]
    
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    print(classification_report(y_val, y_pred, 
                                target_names=["Normal", "Passive Attack"],
                                digits=4))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_val, y_pred)
    print(f"                Predicted")
    print(f"                Normal  Attack")
    print(f"Actual Normal   {cm[0][0]:6d}  {cm[0][1]:6d}")
    print(f"       Attack   {cm[1][0]:6d}  {cm[1][1]:6d}")
    
    # ROC-AUC Score
    auc_score = roc_auc_score(y_val, y_pred_proba)
    print(f"\n🎯 ROC-AUC Score: {auc_score:.4f}")
    
    # Feature importance
    print("\n📊 Feature Importance:")
    feature_importance = sorted(
        zip(FEATURE_NAMES, model.feature_importances_),
        key=lambda x: x[1],
        reverse=True
    )
    for feat, importance in feature_importance:
        print(f"   {feat:30s}: {importance:.4f}")
    
    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': FEATURE_NAMES,
        'auc_score': auc_score
    }
    
    with open(PASSIVE_MODEL_PATH, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✅ Model saved to {PASSIVE_MODEL_PATH}")
    print("=" * 60)


def detect_passive_attack(behavioral_data):
    """
    Detect passive attack from behavioral data
    
    Args:
        behavioral_data: dict with keys matching FEATURE_NAMES
    
    Returns:
        dict with prediction, confidence, and risk_level
    """
    if not os.path.exists(PASSIVE_MODEL_PATH):
        return {
            'error': 'Model not found. Run train_passive_detector() first.',
            'prediction': None
        }
    
    # Load model
    with open(PASSIVE_MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
        model = model_data['model']
        scaler = model_data['scaler']
    
    # Extract features
    features = [behavioral_data[feat] for feat in FEATURE_NAMES]
    features_array = np.array(features).reshape(1, -1)
    
    # Scale and predict
    features_scaled = scaler.transform(features_array)
    prediction = model.predict(features_scaled)[0]
    confidence = model.predict_proba(features_scaled)[0]
    
    # Determine risk level
    attack_probability = confidence[1]
    if attack_probability < 0.3:
        risk_level = "LOW"
    elif attack_probability < 0.7:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
    
    result = {
        'prediction': 'PASSIVE ATTACK DETECTED' if prediction == 1 else 'NORMAL BEHAVIOR',
        'attack_probability': float(attack_probability),
        'normal_probability': float(confidence[0]),
        'risk_level': risk_level,
        'is_attack': bool(prediction == 1)
    }
    
    return result


def test_passive_detector():
    """Test the passive attack detector on test dataset"""
    print("\n" + "=" * 60)
    print("TESTING PASSIVE ATTACK DETECTOR")
    print("=" * 60)
    
    X_test, y_test = load_passive_dataset('passive_test.json')
    
    if X_test is None:
        print("❌ Test failed: Test dataset not found.")
        return
    
    if not os.path.exists(PASSIVE_MODEL_PATH):
        print("❌ Model not found. Train the model first.")
        return
    
    # Load model
    with open(PASSIVE_MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
        model = model_data['model']
        scaler = model_data['scaler']
    
    # Scale and predict
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print(f"\n📊 Test dataset: {len(X_test)} samples")
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(classification_report(y_test, y_pred,
                                target_names=["Normal", "Passive Attack"],
                                digits=4))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"                Predicted")
    print(f"                Normal  Attack")
    print(f"Actual Normal   {cm[0][0]:6d}  {cm[0][1]:6d}")
    print(f"       Attack   {cm[1][0]:6d}  {cm[1][1]:6d}")
    
    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"\n🎯 Test ROC-AUC Score: {auc_score:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    # Train the model
    train_passive_detector()
    
    # Test the model
    test_passive_detector()
    
    # Example detection
    print("\n" + "=" * 60)
    print("EXAMPLE DETECTION")
    print("=" * 60)
    
    # Normal behavior example
    normal_example = {
        'read_ops_per_sec': 12.5,
        'avg_read_block_size': 8192,
        'session_duration': 300.0,
        'decrypt_calls': 5,
        'entropy_of_read_sequence': 0.75,
        'cache_miss_rate': 0.12,
        'reopen_frequency': 1,
        'access_time_zscore': 0.5
    }
    
    print("\n🔍 Testing Normal Behavior:")
    result = detect_passive_attack(normal_example)
    print(f"   Prediction: {result['prediction']}")
    print(f"   Attack Probability: {result['attack_probability']:.4f}")
    print(f"   Risk Level: {result['risk_level']}")
    
    # Attack example
    attack_example = {
        'read_ops_per_sec': 150.0,
        'avg_read_block_size': 128,
        'session_duration': 15.0,
        'decrypt_calls': 250,
        'entropy_of_read_sequence': 0.25,
        'cache_miss_rate': 0.75,
        'reopen_frequency': 35,
        'access_time_zscore': 4.5
    }
    
    print("\n🔍 Testing Suspicious Behavior:")
    result = detect_passive_attack(attack_example)
    print(f"   Prediction: {result['prediction']}")
    print(f"   Attack Probability: {result['attack_probability']:.4f}")
    print(f"   Risk Level: {result['risk_level']}")
    print("=" * 60)
