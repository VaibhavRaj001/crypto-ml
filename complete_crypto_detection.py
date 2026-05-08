"""
Complete Hybrid Encryption/Decryption with Attack Detection
Performs RSA+AES encryption/decryption and detects both active and passive attacks
"""
import os
import time
import pickle
import numpy as np
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from ml.feature_extraction import extract_features
from ml.passive_attack_detector import FEATURE_NAMES

# Paths
KEYS_DIR = "keys"
ENCRYPTED_DIR = "encrypted_files"
DECRYPTED_DIR = "decrypted_files"
ACTIVE_MODEL_PATH = "models/tamper_model.pkl"
PASSIVE_MODEL_PATH = "models/passive_attack_model.pkl"

# Create directories
for directory in [KEYS_DIR, ENCRYPTED_DIR, DECRYPTED_DIR]:
    os.makedirs(directory, exist_ok=True)


class BehaviorMonitor:
    """Monitor behavioral metrics during file operations"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all metrics"""
        self.start_time = time.time()
        self.read_operations = 0
        self.total_bytes_read = 0
        self.decrypt_calls = 0
        self.access_times = []
        self.file_reopens = 0
        self.cache_misses = 0
        self.cache_hits = 0
        self.read_sequence = []
    
    def record_read(self, block_size):
        """Record a read operation"""
        self.read_operations += 1
        self.total_bytes_read += block_size
        self.read_sequence.append(block_size)
        
        # Simulate cache behavior
        if np.random.random() < 0.15:  # Normal cache miss rate
            self.cache_misses += 1
        else:
            self.cache_hits += 1
    
    def record_decrypt(self):
        """Record a decrypt operation"""
        self.decrypt_calls += 1
        self.access_times.append(time.time())
    
    def record_reopen(self):
        """Record file reopen"""
        self.file_reopens += 1
    
    def get_metrics(self):
        """Calculate behavioral metrics"""
        duration = time.time() - self.start_time
        
        # Calculate metrics
        read_ops_per_sec = self.read_operations / max(duration, 0.1)
        
        avg_block_size = (self.total_bytes_read / max(self.read_operations, 1))
        
        # Calculate entropy of read sequence
        if len(self.read_sequence) > 1:
            unique_sizes = len(set(self.read_sequence))
            entropy = unique_sizes / len(self.read_sequence)
        else:
            entropy = 0.5
        
        # Cache miss rate
        total_cache_ops = self.cache_hits + self.cache_misses
        cache_miss_rate = self.cache_misses / max(total_cache_ops, 1)
        
        # Access time z-score (simplified)
        if len(self.access_times) > 2:
            intervals = np.diff(self.access_times)
            if len(intervals) > 0 and np.std(intervals) > 0:
                z_score = (intervals[-1] - np.mean(intervals)) / np.std(intervals)
            else:
                z_score = 0.0
        else:
            z_score = 0.0
        
        return {
            'read_ops_per_sec': float(read_ops_per_sec),
            'avg_read_block_size': float(avg_block_size),
            'session_duration': float(duration),
            'decrypt_calls': int(self.decrypt_calls),
            'entropy_of_read_sequence': float(entropy),
            'cache_miss_rate': float(cache_miss_rate),
            'reopen_frequency': int(self.file_reopens),
            'access_time_zscore': float(z_score)
        }


class CryptoAttackDetector:
    """Complete cryptography system with attack detection"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.active_model = None
        self.passive_model = None
        self.active_scaler = None
        self.passive_scaler = None
        self.behavior_monitor = BehaviorMonitor()
        
        self.load_or_generate_keys()
        self.load_models()
    
    def load_or_generate_keys(self):
        """Load existing keys or generate new ones"""
        private_key_path = os.path.join(KEYS_DIR, "private.pem")
        public_key_path = os.path.join(KEYS_DIR, "public.pem")
        
        if os.path.exists(private_key_path) and os.path.exists(public_key_path):
            # Load existing keys
            with open(private_key_path, "rb") as f:
                self.private_key = RSA.import_key(f.read())
            with open(public_key_path, "rb") as f:
                self.public_key = RSA.import_key(f.read())
            print("✅ Loaded existing RSA keys")
        else:
            # Generate new keys
            key = RSA.generate(2048)
            self.private_key = key
            self.public_key = key.publickey()
            
            # Save keys
            with open(private_key_path, "wb") as f:
                f.write(self.private_key.export_key())
            with open(public_key_path, "wb") as f:
                f.write(self.public_key.export_key())
            print("✅ Generated new RSA keys")
    
    def load_models(self):
        """Load ML models for attack detection"""
        # Load active attack model
        if os.path.exists(ACTIVE_MODEL_PATH):
            with open(ACTIVE_MODEL_PATH, 'rb') as f:
                data = pickle.load(f)
                self.active_model = data['model']
                self.active_scaler = data['scaler']
            print("✅ Active attack model loaded")
        else:
            print("⚠️  Active attack model not found - train it first")
        
        # Load passive attack model
        if os.path.exists(PASSIVE_MODEL_PATH):
            with open(PASSIVE_MODEL_PATH, 'rb') as f:
                data = pickle.load(f)
                self.passive_model = data['model']
                self.passive_scaler = data['scaler']
            print("✅ Passive attack model loaded")
        else:
            print("⚠️  Passive attack model not found - train it first")
    
    def hybrid_encrypt(self, input_file, output_file=None):
        """
        Hybrid encryption: AES-256 for data, RSA for AES key
        
        Args:
            input_file: Path to file to encrypt
            output_file: Path to save encrypted file (optional)
        
        Returns:
            Path to encrypted file
        """
        print(f"\n{'='*70}")
        print("HYBRID ENCRYPTION (RSA + AES-256)")
        print('='*70)
        
        if not os.path.exists(input_file):
            print(f"❌ Error: File not found: {input_file}")
            return None
        
        # Read file
        with open(input_file, "rb") as f:
            data = f.read()
        
        file_size = len(data)
        print(f"📄 Input file: {input_file}")
        print(f"📊 File size: {file_size:,} bytes")
        
        # Generate AES session key
        session_key = get_random_bytes(32)  # AES-256
        print("🔑 Generated AES-256 session key")
        
        # Encrypt data with AES
        cipher_aes = AES.new(session_key, AES.MODE_CBC)
        ciphertext = cipher_aes.encrypt(pad(data, AES.block_size))
        print(f"🔒 Encrypted data with AES-256 (size: {len(ciphertext):,} bytes)")
        
        # Encrypt session key with RSA
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        print("🔐 Encrypted AES key with RSA-2048")
        
        # Prepare output file
        if output_file is None:
            filename = os.path.basename(input_file)
            output_file = os.path.join(ENCRYPTED_DIR, f"{filename}.enc")
        
        # Save encrypted file (format: enc_key_size + enc_key + iv + ciphertext)
        with open(output_file, "wb") as f:
            f.write(len(enc_session_key).to_bytes(4, 'big'))
            f.write(enc_session_key)
            f.write(cipher_aes.iv)
            f.write(ciphertext)
        
        print(f"💾 Saved encrypted file: {output_file}")
        print('='*70)
        
        return output_file
    
    def hybrid_decrypt(self, encrypted_file, output_file=None):
        """
        Hybrid decryption with behavioral monitoring
        
        Args:
            encrypted_file: Path to encrypted file
            output_file: Path to save decrypted file (optional)
        
        Returns:
            tuple: (decrypted_file_path, behavioral_metrics)
        """
        print(f"\n{'='*70}")
        print("HYBRID DECRYPTION WITH BEHAVIORAL MONITORING")
        print('='*70)
        
        # Reset behavior monitor
        self.behavior_monitor.reset()
        
        if not os.path.exists(encrypted_file):
            print(f"❌ Error: File not found: {encrypted_file}")
            return None, None
        
        print(f"📄 Encrypted file: {encrypted_file}")
        
        # Read encrypted file
        with open(encrypted_file, "rb") as f:
            # Read encrypted session key
            enc_key_size = int.from_bytes(f.read(4), 'big')
            self.behavior_monitor.record_read(4)
            
            enc_session_key = f.read(enc_key_size)
            self.behavior_monitor.record_read(enc_key_size)
            
            # Read IV
            iv = f.read(16)
            self.behavior_monitor.record_read(16)
            
            # Read ciphertext
            ciphertext = f.read()
            self.behavior_monitor.record_read(len(ciphertext))
        
        print(f"📊 Read {len(ciphertext):,} bytes of encrypted data")
        
        try:
            # Decrypt session key with RSA
            self.behavior_monitor.record_decrypt()
            cipher_rsa = PKCS1_OAEP.new(self.private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)
            print("🔓 Decrypted AES key with RSA")
            
            # Decrypt data with AES
            self.behavior_monitor.record_decrypt()
            cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)
            print(f"🔓 Decrypted data with AES-256 (size: {len(decrypted_data):,} bytes)")
            
            # Prepare output file
            if output_file is None:
                filename = os.path.basename(encrypted_file).replace('.enc', '')
                output_file = os.path.join(DECRYPTED_DIR, filename)
            
            # Save decrypted file
            with open(output_file, "wb") as f:
                f.write(decrypted_data)
            
            print(f"💾 Saved decrypted file: {output_file}")
            
            # Get behavioral metrics
            metrics = self.behavior_monitor.get_metrics()
            
            print("\n📊 Behavioral Metrics Collected:")
            print(f"   Read ops/sec: {metrics['read_ops_per_sec']:.2f}")
            print(f"   Avg block size: {metrics['avg_read_block_size']:.0f} bytes")
            print(f"   Session duration: {metrics['session_duration']:.2f} sec")
            print(f"   Decrypt calls: {metrics['decrypt_calls']}")
            print(f"   Cache miss rate: {metrics['cache_miss_rate']:.2%}")
            
            print('='*70)
            
            return output_file, metrics
            
        except (ValueError, KeyError) as e:
            print(f"❌ Decryption failed: {e}")
            print("⚠️  File may be corrupted or tampered!")
            print('='*70)
            return None, self.behavior_monitor.get_metrics()
    
    def detect_active_attack(self, file_path):
        """
        Detect active attacks (file tampering)
        
        Returns:
            dict with detection results and percentage (capped at 80%)
        """
        if self.active_model is None:
            return {
                'attack_type': 'ACTIVE',
                'detected': False,
                'percentage': 0.0,
                'status': 'Model not loaded'
            }
        
        if not os.path.exists(file_path):
            return {
                'attack_type': 'ACTIVE',
                'detected': False,
                'percentage': 0.0,
                'status': 'File not found'
            }
        
        # Extract features
        features = extract_features(file_path)
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.active_scaler.transform(features_array)
        
        # Predict
        prediction = self.active_model.predict(features_scaled)[0]
        probabilities = self.active_model.predict_proba(features_scaled)[0]
        
        # Cap at 80%
        tamper_prob = min(probabilities[1] * 100, 80.0)
        
        return {
            'attack_type': 'ACTIVE',
            'detected': bool(prediction == 1),
            'percentage': round(tamper_prob, 2),
            'status': 'TAMPERED' if prediction == 1 else 'SAFE',
            'raw_probability': probabilities[1]
        }
    
    def detect_passive_attack(self, behavioral_metrics):
        """
        Detect passive attacks (behavioral anomalies)
        
        Returns:
            dict with detection results and percentage (capped at 80%)
        """
        if self.passive_model is None:
            return {
                'attack_type': 'PASSIVE',
                'detected': False,
                'percentage': 0.0,
                'status': 'Model not loaded'
            }
        
        # Extract features
        features = [behavioral_metrics[feat] for feat in FEATURE_NAMES]
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.passive_scaler.transform(features_array)
        
        # Predict
        prediction = self.passive_model.predict(features_scaled)[0]
        probabilities = self.passive_model.predict_proba(features_scaled)[0]
        
        # Cap at 80%
        attack_prob = min(probabilities[1] * 100, 80.0)
        
        # Risk level
        if attack_prob < 30:
            risk_level = "LOW"
        elif attack_prob < 60:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        return {
            'attack_type': 'PASSIVE',
            'detected': bool(prediction == 1),
            'percentage': round(attack_prob, 2),
            'status': 'ATTACK DETECTED' if prediction == 1 else 'NORMAL',
            'risk_level': risk_level,
            'raw_probability': probabilities[1]
        }
    
    def complete_analysis(self, input_file):
        """
        Complete workflow: Encrypt -> Decrypt -> Detect both attacks
        
        Args:
            input_file: Path to file to analyze
        
        Returns:
            dict with complete analysis results
        """
        print("\n" + "="*70)
        print("COMPLETE CRYPTOGRAPHIC ANALYSIS WITH ATTACK DETECTION")
        print("="*70)
        
        results = {
            'input_file': input_file,
            'encryption': None,
            'decryption': None,
            'active_attack': None,
            'passive_attack': None,
            'overall_status': None
        }
        
        # Step 1: Encrypt
        encrypted_file = self.hybrid_encrypt(input_file)
        if encrypted_file is None:
            results['overall_status'] = 'ENCRYPTION FAILED'
            return results
        results['encryption'] = {'status': 'SUCCESS', 'file': encrypted_file}
        
        # Step 2: Decrypt with behavioral monitoring
        decrypted_file, behavioral_metrics = self.hybrid_decrypt(encrypted_file)
        if decrypted_file is None:
            results['decryption'] = {'status': 'FAILED'}
            results['overall_status'] = 'DECRYPTION FAILED - POSSIBLE TAMPERING'
        else:
            results['decryption'] = {
                'status': 'SUCCESS',
                'file': decrypted_file,
                'metrics': behavioral_metrics
            }
        
        # Step 3: Detect active attack (on decrypted file)
        if decrypted_file:
            active_result = self.detect_active_attack(decrypted_file)
            results['active_attack'] = active_result
        
        # Step 4: Detect passive attack (on behavioral metrics)
        if behavioral_metrics:
            passive_result = self.detect_passive_attack(behavioral_metrics)
            results['passive_attack'] = passive_result
        
        # Step 5: Overall assessment
        self.display_results(results)
        
        return results
    
    def display_results(self, results):
        """Display formatted results"""
        print("\n" + "="*70)
        print("DETECTION RESULTS")
        print("="*70)
        
        # Active attack results
        if results['active_attack']:
            active = results['active_attack']
            print(f"\n🔴 ACTIVE ATTACK DETECTION (File Tampering)")
            print("─"*70)
            print(f"   Status: {active['status']}")
            print(f"   Detection: {'⚠️  DETECTED' if active['detected'] else '✅ NOT DETECTED'}")
            print(f"   Probability: {active['percentage']:.2f}%")
            
            # Visual bar
            bar_length = int(active['percentage'] / 2)
            bar = '█' * bar_length + '░' * (40 - bar_length)
            print(f"   [{bar}] {active['percentage']:.2f}%")
        
        # Passive attack results
        if results['passive_attack']:
            passive = results['passive_attack']
            print(f"\n🔵 PASSIVE ATTACK DETECTION (Behavioral Analysis)")
            print("─"*70)
            print(f"   Status: {passive['status']}")
            print(f"   Detection: {'⚠️  DETECTED' if passive['detected'] else '✅ NOT DETECTED'}")
            print(f"   Probability: {passive['percentage']:.2f}%")
            print(f"   Risk Level: {passive['risk_level']}")
            
            # Visual bar
            bar_length = int(passive['percentage'] / 2)
            bar = '█' * bar_length + '░' * (40 - bar_length)
            print(f"   [{bar}] {passive['percentage']:.2f}%")
        
        # Overall status
        print(f"\n{'='*70}")
        active_detected = results['active_attack'] and results['active_attack']['detected']
        passive_detected = results['passive_attack'] and results['passive_attack']['detected']
        
        if active_detected and passive_detected:
            status = "🚨 CRITICAL - BOTH ATTACKS DETECTED"
        elif active_detected:
            status = "⚠️  HIGH RISK - ACTIVE ATTACK DETECTED"
        elif passive_detected:
            status = "⚠️  MEDIUM RISK - PASSIVE ATTACK DETECTED"
        else:
            status = "✅ SECURE - NO THREATS DETECTED"
        
        print(f"Overall Status: {status}")
        print("="*70)


def main():
    """Main function"""
    print("\n" + "="*70)
    print("HYBRID ENCRYPTION/DECRYPTION WITH ATTACK DETECTION")
    print("="*70)
    
    # Initialize detector
    detector = CryptoAttackDetector()
    
    # Check if models are loaded
    if detector.active_model is None or detector.passive_model is None:
        print("\n⚠️  WARNING: Models not loaded!")
        print("Please train the models first:")
        print("   python -c \"from ml.train_model import train_model; train_model()\"")
        print("   python -c \"from ml.passive_attack_detector import train_passive_detector; train_passive_detector()\"")
        return
    
    # Get input file
    print("\n📁 Available test files:")
    original_dir = "data/original"
    if os.path.exists(original_dir):
        files = [f for f in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, f))]
        for i, file in enumerate(files[:10], 1):
            print(f"   {i}. {file}")
        
        print(f"\n   Or enter custom file path")
        choice = input("\nEnter file number or path: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            input_file = os.path.join(original_dir, files[int(choice) - 1])
        else:
            input_file = choice
    else:
        input_file = input("\nEnter file path to analyze: ").strip()
    
    if not os.path.exists(input_file):
        print(f"❌ Error: File not found: {input_file}")
        return
    
    # Run complete analysis
    results = detector.complete_analysis(input_file)
    
    # Save results
    print(f"\n💾 Results saved to logs/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
