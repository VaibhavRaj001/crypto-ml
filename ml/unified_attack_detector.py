"""
Unified Attack Detection System
Combines Active (tampering) and Passive (behavioral) attack detection
"""
import os
import json
import pickle
import numpy as np
from datetime import datetime
from feature_extraction import extract_features
from passive_attack_detector import detect_passive_attack, FEATURE_NAMES

ACTIVE_MODEL_PATH = "models/tamper_model.pkl"
PASSIVE_MODEL_PATH = "models/passive_attack_model.pkl"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


class UnifiedAttackDetector:
    """
    Unified detector for both active and passive attacks
    """
    
    def __init__(self):
        self.active_model = None
        self.passive_model = None
        self.active_scaler = None
        self.passive_scaler = None
        self.load_models()
    
    def load_models(self):
        """Load both active and passive attack detection models"""
        # Load active attack model
        if os.path.exists(ACTIVE_MODEL_PATH):
            with open(ACTIVE_MODEL_PATH, 'rb') as f:
                data = pickle.load(f)
                self.active_model = data['model']
                self.active_scaler = data['scaler']
            print("✅ Active attack model loaded")
        else:
            print("⚠️  Active attack model not found")
        
        # Load passive attack model
        if os.path.exists(PASSIVE_MODEL_PATH):
            with open(PASSIVE_MODEL_PATH, 'rb') as f:
                data = pickle.load(f)
                self.passive_model = data['model']
                self.passive_scaler = data['scaler']
            print("✅ Passive attack model loaded")
        else:
            print("⚠️  Passive attack model not found")
    
    def detect_active_attack(self, file_path):
        """
        Detect active attacks (file tampering)
        
        Args:
            file_path: Path to file to check
        
        Returns:
            dict with detection results
        """
        if self.active_model is None:
            return {
                'type': 'ACTIVE',
                'error': 'Active attack model not loaded',
                'is_attack': None
            }
        
        if not os.path.exists(file_path):
            return {
                'type': 'ACTIVE',
                'error': f'File not found: {file_path}',
                'is_attack': None
            }
        
        # Extract file features
        features = extract_features(file_path)
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.active_scaler.transform(features_array)
        
        # Predict
        prediction = self.active_model.predict(features_scaled)[0]
        confidence = self.active_model.predict_proba(features_scaled)[0]
        
        return {
            'type': 'ACTIVE',
            'prediction': 'TAMPERED' if prediction == 1 else 'SAFE',
            'is_attack': bool(prediction == 1),
            'tamper_probability': float(confidence[1]),
            'safe_probability': float(confidence[0]),
            'file_path': file_path
        }
    
    def detect_passive_attack(self, behavioral_data):
        """
        Detect passive attacks (behavioral anomalies)
        
        Args:
            behavioral_data: dict with behavioral metrics
        
        Returns:
            dict with detection results
        """
        if self.passive_model is None:
            return {
                'type': 'PASSIVE',
                'error': 'Passive attack model not loaded',
                'is_attack': None
            }
        
        # Validate behavioral data
        for feat in FEATURE_NAMES:
            if feat not in behavioral_data:
                return {
                    'type': 'PASSIVE',
                    'error': f'Missing feature: {feat}',
                    'is_attack': None
                }
        
        # Extract features
        features = [behavioral_data[feat] for feat in FEATURE_NAMES]
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.passive_scaler.transform(features_array)
        
        # Predict
        prediction = self.passive_model.predict(features_scaled)[0]
        confidence = self.passive_model.predict_proba(features_scaled)[0]
        
        # Risk level
        attack_probability = confidence[1]
        if attack_probability < 0.3:
            risk_level = "LOW"
        elif attack_probability < 0.7:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        return {
            'type': 'PASSIVE',
            'prediction': 'PASSIVE ATTACK' if prediction == 1 else 'NORMAL',
            'is_attack': bool(prediction == 1),
            'attack_probability': float(attack_probability),
            'normal_probability': float(confidence[0]),
            'risk_level': risk_level,
            'behavioral_data': behavioral_data
        }
    
    def comprehensive_check(self, file_path, behavioral_data):
        """
        Perform comprehensive security check (both active and passive)
        
        Args:
            file_path: Path to file to check
            behavioral_data: dict with behavioral metrics
        
        Returns:
            dict with comprehensive results
        """
        print("\n" + "=" * 70)
        print("COMPREHENSIVE SECURITY ANALYSIS")
        print("=" * 70)
        
        # Active attack detection
        print("\n🔍 Checking for Active Attacks (File Tampering)...")
        active_result = self.detect_active_attack(file_path)
        
        # Passive attack detection
        print("🔍 Checking for Passive Attacks (Behavioral Anomalies)...")
        passive_result = self.detect_passive_attack(behavioral_data)
        
        # Overall threat assessment
        active_threat = active_result.get('is_attack', False)
        passive_threat = passive_result.get('is_attack', False)
        
        if active_threat and passive_threat:
            overall_status = "CRITICAL - BOTH ATTACKS DETECTED"
            threat_level = "CRITICAL"
        elif active_threat:
            overall_status = "HIGH RISK - ACTIVE ATTACK DETECTED"
            threat_level = "HIGH"
        elif passive_threat:
            overall_status = "MEDIUM RISK - PASSIVE ATTACK DETECTED"
            threat_level = "MEDIUM"
        else:
            overall_status = "SECURE - NO THREATS DETECTED"
            threat_level = "LOW"
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall_status,
            'threat_level': threat_level,
            'active_attack': active_result,
            'passive_attack': passive_result,
            'recommendations': self._generate_recommendations(active_result, passive_result)
        }
        
        # Display results
        self._display_results(result)
        
        # Log results
        self._log_results(result)
        
        return result
    
    def _generate_recommendations(self, active_result, passive_result):
        """Generate security recommendations based on detection results"""
        recommendations = []
        
        if active_result.get('is_attack'):
            recommendations.append("🚨 File integrity compromised - Do not use this file")
            recommendations.append("🔒 Verify file source and obtain clean copy")
            recommendations.append("🔍 Investigate how file was tampered")
        
        if passive_result.get('is_attack'):
            risk = passive_result.get('risk_level', 'UNKNOWN')
            recommendations.append(f"⚠️  Suspicious behavioral pattern detected (Risk: {risk})")
            recommendations.append("🛡️  Monitor system for unauthorized access")
            recommendations.append("🔐 Review access logs and authentication records")
            
            # Specific recommendations based on behavioral patterns
            bd = passive_result.get('behavioral_data', {})
            if bd.get('read_ops_per_sec', 0) > 100:
                recommendations.append("📊 Abnormally high read rate - possible timing attack")
            if bd.get('cache_miss_rate', 0) > 0.6:
                recommendations.append("💾 High cache miss rate - possible cache side-channel attack")
            if bd.get('decrypt_calls', 0) > 100:
                recommendations.append("🔓 Excessive decrypt attempts - possible key extraction attempt")
        
        if not recommendations:
            recommendations.append("✅ System appears secure")
            recommendations.append("✅ Continue normal operations")
        
        return recommendations
    
    def _display_results(self, result):
        """Display formatted results"""
        print("\n" + "=" * 70)
        print("DETECTION RESULTS")
        print("=" * 70)
        
        print(f"\n⏰ Timestamp: {result['timestamp']}")
        print(f"🎯 Overall Status: {result['overall_status']}")
        print(f"⚠️  Threat Level: {result['threat_level']}")
        
        # Active attack results
        print("\n" + "-" * 70)
        print("ACTIVE ATTACK DETECTION (File Tampering)")
        print("-" * 70)
        active = result['active_attack']
        if 'error' in active:
            print(f"❌ Error: {active['error']}")
        else:
            print(f"File: {active.get('file_path', 'N/A')}")
            print(f"Status: {active['prediction']}")
            print(f"Tamper Probability: {active.get('tamper_probability', 0):.2%}")
        
        # Passive attack results
        print("\n" + "-" * 70)
        print("PASSIVE ATTACK DETECTION (Behavioral Analysis)")
        print("-" * 70)
        passive = result['passive_attack']
        if 'error' in passive:
            print(f"❌ Error: {passive['error']}")
        else:
            print(f"Status: {passive['prediction']}")
            print(f"Attack Probability: {passive.get('attack_probability', 0):.2%}")
            print(f"Risk Level: {passive.get('risk_level', 'N/A')}")
        
        # Recommendations
        print("\n" + "-" * 70)
        print("RECOMMENDATIONS")
        print("-" * 70)
        for rec in result['recommendations']:
            print(f"  {rec}")
        
        print("\n" + "=" * 70)
    
    def _log_results(self, result):
        """Log detection results to file"""
        log_file = os.path.join(LOG_DIR, f"detection_log_{datetime.now().strftime('%Y%m%d')}.json")
        
        # Load existing logs
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Append new result
        logs.append(result)
        
        # Save logs
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"\n📝 Results logged to: {log_file}")


def main():
    """Main function for testing unified detector"""
    detector = UnifiedAttackDetector()
    
    # Example 1: Check a file with normal behavior
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Normal File + Normal Behavior")
    print("=" * 70)
    
    test_file = "data/original/cryptography_ml_ideas.pdf"
    normal_behavior = {
        'read_ops_per_sec': 12.5,
        'avg_read_block_size': 8192,
        'session_duration': 300.0,
        'decrypt_calls': 5,
        'entropy_of_read_sequence': 0.75,
        'cache_miss_rate': 0.12,
        'reopen_frequency': 1,
        'access_time_zscore': 0.5
    }
    
    if os.path.exists(test_file):
        detector.comprehensive_check(test_file, normal_behavior)
    else:
        print(f"⚠️  Test file not found: {test_file}")
    
    # Example 2: Check a tampered file with suspicious behavior
    print("\n\n" + "=" * 70)
    print("EXAMPLE 2: Tampered File + Suspicious Behavior")
    print("=" * 70)
    
    tampered_file = "data/tampered/cryptography_ml_ideas.pdf_flip"
    suspicious_behavior = {
        'read_ops_per_sec': 180.0,
        'avg_read_block_size': 256,
        'session_duration': 20.0,
        'decrypt_calls': 350,
        'entropy_of_read_sequence': 0.28,
        'cache_miss_rate': 0.78,
        'reopen_frequency': 45,
        'access_time_zscore': 5.2
    }
    
    if os.path.exists(tampered_file):
        detector.comprehensive_check(tampered_file, suspicious_behavior)
    else:
        print(f"⚠️  Test file not found: {tampered_file}")


if __name__ == "__main__":
    main()
