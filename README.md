# Hybrid Encryption with ML-Based Attack Detection

A complete cryptographic system that combines **RSA-2048 + AES-256 hybrid encryption** with **machine learning-based attack detection** for both active (file tampering) and passive (behavioral/side-channel) attacks.

## 🎯 What This System Does

1. **Encrypts files** using hybrid RSA + AES encryption
2. **Decrypts files** while monitoring behavioral patterns
3. **Detects active attacks** (file tampering) with percentage score
4. **Detects passive attacks** (eavesdropping, timing attacks) with percentage score
5. **Provides comprehensive security analysis** with visual results

## ✨ Key Features

- ✅ **Hybrid Encryption:** RSA-2048 for key exchange + AES-256 for data
- ✅ **Dual Attack Detection:** Both active and passive threats
- ✅ **8 Behavioral Vectors:** Comprehensive behavioral monitoring
- ✅ **ML-Powered:** Gradient Boosting + Random Forest classifiers
- ✅ **Real-time Monitoring:** Behavioral analysis during decryption
- ✅ **Percentage Scores:** Attack probability (capped at 80%)
- ✅ **Visual Results:** Progress bars and formatted output

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install numpy scikit-learn pycryptodome
```

### 2. First-Time Setup
```bash
python run_complete_system.py
```
Select **Option 8: Run Complete Pipeline**

This will:
- Generate training datasets (active + passive attacks)
- Train both ML models
- Test the detectors

### 3. Run the Demo
```bash
python run_crypto_demo.py
```

**That's it!** The system will encrypt a file, decrypt it, and show attack detection results.

## 📊 Example Output

```
DETECTION RESULTS
======================================================================

🔴 ACTIVE ATTACK DETECTION (File Tampering)
──────────────────────────────────────────────────────────────────────
   Status: SAFE
   Detection: ✅ NOT DETECTED
   Probability: 34.50%
   [█████████████████░░░░░░░░░░░░░░░░░░░░░░░] 34.50%

🔵 PASSIVE ATTACK DETECTION (Behavioral Analysis)
──────────────────────────────────────────────────────────────────────
   Status: NORMAL
   Detection: ✅ NOT DETECTED
   Probability: 0.04%
   Risk Level: LOW
   [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0.04%

======================================================================
Overall Status: ✅ SECURE - NO THREATS DETECTED
======================================================================
```

## 🎮 Usage Options

### Option 1: Automated Demo (Recommended)
```bash
python run_crypto_demo.py
```
Tests a file from `data/original/` automatically.

### Option 2: Interactive Mode
```bash
python run_crypto_demo.py --interactive
```
Choose files interactively from menu.

### Option 3: Test Specific File
```bash
python run_crypto_demo.py "path/to/your/file.pdf"
```

### Option 4: Full System Menu
```bash
python run_complete_system.py
```
Access all system functions (training, testing, status).

## 🔍 What Gets Detected

### Active Attacks (File Tampering)
- **Byte flipping** - Random bit modifications
- **Data truncation** - Removing portions of data
- **Noise injection** - Appending random data
- **Block shuffling** - Reordering data blocks

**Detection Method:** Analyzes file properties (size, entropy, byte distribution)

### Passive Attacks (Behavioral/Side-Channel)
- **Timing attacks** - Measuring operation times to extract keys
- **Cache attacks** - Analyzing cache behavior patterns
- **Power analysis** - Monitoring power consumption patterns
- **Memory dumping** - Bulk memory reading attempts

**Detection Method:** Monitors 8 behavioral vectors during decryption

## 📈 The 8 Behavioral Vectors

During decryption, the system monitors:

| # | Vector | What It Measures | Normal | Attack |
|---|--------|------------------|--------|--------|
| 1 | **read_ops_per_sec** | Operation frequency | 5-20 | >50 |
| 2 | **avg_read_block_size** | Data chunk size | 4K-16K | <512 |
| 3 | **session_duration** | Operation time | 60-600s | <30s |
| 4 | **decrypt_calls** | Decryption count | 1-10 | >100 |
| 5 | **entropy_of_read_sequence** | Access randomness | 0.6-0.85 | <0.4 |
| 6 | **cache_miss_rate** | Cache efficiency | 5-20% | >60% |
| 7 | **reopen_frequency** | File reopens | 0-3 | >20 |
| 8 | **access_time_zscore** | Timing anomaly | -1.5 to 1.5 | >2.5 |

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT FILE                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│         HYBRID ENCRYPTION (RSA-2048 + AES-256)          │
│  • Generate AES-256 session key                         │
│  • Encrypt file with AES-256                            │
│  • Encrypt AES key with RSA-2048                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              ENCRYPTED FILE STORAGE                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│    HYBRID DECRYPTION + BEHAVIORAL MONITORING            │
│  • Monitor 8 behavioral vectors                         │
│  • Decrypt RSA key                                      │
│  • Decrypt AES data                                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              DUAL ATTACK DETECTION                      │
├─────────────────────────────────────────────────────────┤
│  🔴 ACTIVE DETECTION    │  🔵 PASSIVE DETECTION         │
│  (File Analysis)        │  (Behavior Analysis)          │
│  • Random Forest        │  • Gradient Boosting          │
│  • 6 file features      │  • 8 behavioral vectors       │
│  • Tampering detection  │  • Side-channel detection     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              SECURITY ASSESSMENT                        │
│  • Active attack probability (0-80%)                    │
│  • Passive attack probability (0-80%)                   │
│  • Overall threat level                                 │
│  • Recommendations                                      │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
crypto-ml/
├── 🎮 Main Scripts
│   ├── run_crypto_demo.py              # Main demo script ⭐
│   ├── complete_crypto_detection.py    # Core detection system
│   └── run_complete_system.py          # Setup & management
│
├── 🤖 ML Modules
│   └── ml/
│       ├── passive_attack_detector.py  # Passive detection
│       ├── detect_tamper.py            # Active detection
│       ├── unified_attack_detector.py  # Combined detection
│       ├── feature_extraction.py       # Feature extraction
│       └── train_model.py              # Model training
│
├── 🔧 Data Generation
│   ├── passive_data_generator.py       # Behavioral data
│   └── tempered_generator.py           # Tampered files
│
├── 📊 Data & Models
│   ├── data/
│   │   ├── original/                   # Clean files
│   │   ├── tampered/                   # Tampered files
│   │   └── passive_attacks/            # Behavioral data
│   ├── models/
│   │   ├── tamper_model.pkl            # Active model
│   │   └── passive_attack_model.pkl    # Passive model
│   ├── encrypted_files/                # Encrypted outputs
│   ├── decrypted_files/                # Decrypted outputs
│   └── keys/                           # RSA keys
│
└── 📄 Documentation
    ├── README.md                       # This file
    ├── HOW_TO_RUN.md                   # Detailed instructions
    ├── QUICK_START.md                  # Quick start guide
    ├── SYSTEM_SUMMARY.md               # System overview
    ├── ATTACK_COMPARISON.md            # Attack types explained
    └── INDEX.md                        # Complete navigation
```

## 🔧 Advanced Usage

### Python API

```python
from complete_crypto_detection import CryptoAttackDetector

# Initialize
detector = CryptoAttackDetector()

# Encrypt a file
encrypted_file = detector.hybrid_encrypt("document.pdf")

# Decrypt with monitoring
decrypted_file, metrics = detector.hybrid_decrypt(encrypted_file)

# Detect active attack
active_result = detector.detect_active_attack(decrypted_file)
print(f"Active: {active_result['percentage']:.2f}%")

# Detect passive attack
passive_result = detector.detect_passive_attack(metrics)
print(f"Passive: {passive_result['percentage']:.2f}%")

# Complete analysis
results = detector.complete_analysis("document.pdf")
```

### Custom Behavioral Testing

```python
# Test with custom behavioral pattern
custom_metrics = {
    'read_ops_per_sec': 150.0,
    'avg_read_block_size': 256,
    'session_duration': 20.0,
    'decrypt_calls': 300,
    'entropy_of_read_sequence': 0.3,
    'cache_miss_rate': 0.75,
    'reopen_frequency': 40,
    'access_time_zscore': 4.5
}

result = detector.detect_passive_attack(custom_metrics)
print(f"Attack probability: {result['percentage']:.2f}%")
```

## 📊 Model Performance

### Passive Attack Detection
- **Algorithm:** Gradient Boosting Classifier
- **Accuracy:** 100% on test set
- **ROC-AUC:** 1.0000
- **Features:** 8 behavioral vectors

### Active Attack Detection
- **Algorithm:** Random Forest Classifier
- **Features:** 6 file-based vectors
- **Training samples:** 70 (14 original + 56 tampered)

## 🛠️ Troubleshooting

### "Models not loaded"
```bash
python run_complete_system.py
# Select Option 8: Run Complete Pipeline
```

### "No files found"
Add test files to `data/original/` directory.

### Import errors
```bash
pip install numpy scikit-learn pycryptodome
```

## 📚 Documentation

- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - Detailed running instructions
- **[QUICK_START.md](QUICK_START.md)** - 5-minute quick start
- **[SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)** - System overview
- **[ATTACK_COMPARISON.md](ATTACK_COMPARISON.md)** - Active vs Passive attacks
- **[INDEX.md](INDEX.md)** - Complete file navigation

## 🎓 Key Concepts

### Why Hybrid Encryption?
- **RSA:** Secure key exchange (slow, small data)
- **AES:** Fast bulk encryption (fast, large data)
- **Combined:** Best of both worlds

### Why Both Detection Types?
- **Active attacks** modify data → Detected by file analysis
- **Passive attacks** observe data → Detected by behavior analysis
- **Together:** Comprehensive security coverage

### Why 8 Behavioral Vectors?
Each vector captures a different attack signature:
- **Frequency** metrics detect rapid probing
- **Size** metrics detect targeted access
- **Timing** metrics detect side-channel attacks
- **Pattern** metrics detect systematic scanning

## 🎯 Use Cases

1. **Secure File Storage** - Encrypt sensitive files with attack detection
2. **Data Transmission** - Detect tampering during transfer
3. **Security Monitoring** - Real-time behavioral analysis
4. **Forensic Analysis** - Identify attack patterns
5. **Research & Education** - Learn about cryptography and ML security

## 🔒 Security Features

- ✅ RSA-2048 key exchange
- ✅ AES-256 data encryption
- ✅ CBC mode with random IV
- ✅ PKCS7 padding
- ✅ Secure key generation
- ✅ ML-based anomaly detection
- ✅ Real-time behavioral monitoring
- ✅ Comprehensive logging

## 📞 Quick Reference

```bash
# Setup (first time)
pip install numpy scikit-learn pycryptodome
python run_complete_system.py  # Option 8

# Run demo
python run_crypto_demo.py

# Interactive mode
python run_crypto_demo.py --interactive

# Test specific file
python run_crypto_demo.py "file.pdf"

# Check status
python run_complete_system.py  # Option 9
```

## 🎉 Summary

This system provides:
- ✅ **Military-grade encryption** (RSA-2048 + AES-256)
- ✅ **Dual attack detection** (Active + Passive)
- ✅ **Real-time monitoring** (8 behavioral vectors)
- ✅ **ML-powered analysis** (100% accuracy on test set)
- ✅ **Easy to use** (3-step setup, 1 command to run)
- ✅ **Comprehensive output** (Percentages, visual bars, recommendations)

**Ready to start?** Run: `python run_crypto_demo.py`

---

**Version:** 1.0.0  
**Last Updated:** May 2026  
**License:** MIT  
**Built with:** Python, scikit-learn, PyCryptodome
