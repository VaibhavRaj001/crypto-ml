# Cryptography + ML Attack Detection System

A comprehensive machine learning system for detecting both **Active** and **Passive** attacks on encrypted data.

## 🎯 Overview

This system provides dual-layer security detection:

### 1. **Active Attack Detection** (File Tampering)
Detects modifications to encrypted files using file-based features:
- File size analysis
- Entropy calculation
- Byte distribution statistics
- File format validation

**Attack Types Detected:**
- Byte flipping
- Data truncation
- Noise injection
- Block shuffling

### 2. **Passive Attack Detection** (Behavioral Analysis)
Detects eavesdropping and side-channel attacks using 8 behavioral vectors:

| Vector | Description | Normal Range | Attack Pattern |
|--------|-------------|--------------|----------------|
| `read_ops_per_sec` | Read operations per second | 5-20 | >50 (rapid probing) |
| `avg_read_block_size` | Average block size in bytes | 4096-16384 | <512 (timing attacks) |
| `session_duration` | Session length in seconds | 60-600 | <30 (quick bursts) |
| `decrypt_calls` | Number of decrypt operations | 1-10 | >100 (key extraction) |
| `entropy_of_read_sequence` | Randomness of access pattern | 0.6-0.85 | <0.4 (repetitive) |
| `cache_miss_rate` | Cache miss percentage | 0.05-0.20 | >0.6 (cache attacks) |
| `reopen_frequency` | File reopen count | 0-3 | >20 (probing) |
| `access_time_zscore` | Timing anomaly score | -1.5 to 1.5 | >2.5 (anomalous) |

**Attack Types Detected:**
- Timing attacks
- Cache side-channel attacks
- Power analysis attacks
- Memory dumping attempts

## 📁 Project Structure

```
crypto-ml/
├── data/
│   ├── original/              # Original clean files
│   ├── tampered/              # Tampered files (active attacks)
│   └── passive_attacks/       # Behavioral data (passive attacks)
│       ├── passive_train.json
│       ├── passive_test.json
│       ├── normal_behavior.json
│       └── passive_attacks.json
├── ml/
│   ├── feature_extraction.py        # Active attack features
│   ├── train_model.py               # Active detector training
│   ├── detect_tamper.py             # Active attack detection
│   ├── passive_attack_detector.py   # Passive detector (train + detect)
│   └── unified_attack_detector.py   # Combined detection system
├── models/
│   ├── tamper_model.pkl             # Active attack model
│   └── passive_attack_model.pkl     # Passive attack model
├── logs/                            # Detection logs
├── tempered_generator.py            # Generate active attack data
├── passive_data_generator.py        # Generate passive attack data
└── run_complete_system.py           # Main interface
```

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Complete System

```bash
python run_complete_system.py
```

This launches an interactive menu with options to:
1. Generate datasets
2. Train models
3. Test detectors
4. Run unified detection
5. View system status

### Quick Pipeline (All-in-One)

```bash
# Option 8 in the menu runs everything:
# - Generate both datasets
# - Train both models
# - Test both detectors
```

## 📊 Usage Examples

### 1. Generate Datasets

```python
# Generate active attack dataset (tampered files)
python tempered_generator.py

# Generate passive attack dataset (behavioral data)
python passive_data_generator.py
```

### 2. Train Models

```python
# Train active attack detector
from ml.train_model import train_model
train_model()

# Train passive attack detector
from ml.passive_attack_detector import train_passive_detector
train_passive_detector()
```

### 3. Detect Active Attacks

```python
from ml.detect_tamper import detect_tampering

result = detect_tampering("data/tampered/file.pdf_flip")
print(result)  # "✅ File is SAFE" or "❌ File is TAMPERED"
```

### 4. Detect Passive Attacks

```python
from ml.passive_attack_detector import detect_passive_attack

behavioral_data = {
    'read_ops_per_sec': 150.0,
    'avg_read_block_size': 256,
    'session_duration': 20.0,
    'decrypt_calls': 300,
    'entropy_of_read_sequence': 0.25,
    'cache_miss_rate': 0.75,
    'reopen_frequency': 40,
    'access_time_zscore': 4.5
}

result = detect_passive_attack(behavioral_data)
print(result['prediction'])  # "NORMAL BEHAVIOR" or "PASSIVE ATTACK DETECTED"
print(f"Risk Level: {result['risk_level']}")  # LOW, MEDIUM, or HIGH
```

### 5. Unified Detection (Both Attacks)

```python
from ml.unified_attack_detector import UnifiedAttackDetector

detector = UnifiedAttackDetector()

# Check file + behavior simultaneously
result = detector.comprehensive_check(
    file_path="data/original/document.pdf",
    behavioral_data={
        'read_ops_per_sec': 12.5,
        'avg_read_block_size': 8192,
        'session_duration': 300.0,
        'decrypt_calls': 5,
        'entropy_of_read_sequence': 0.75,
        'cache_miss_rate': 0.12,
        'reopen_frequency': 1,
        'access_time_zscore': 0.5
    }
)

print(result['overall_status'])
print(result['threat_level'])
```

## 🧪 Model Performance

### Active Attack Detector
- **Algorithm:** Random Forest Classifier
- **Features:** 6 (file size, entropy, byte statistics, format)
- **Expected Accuracy:** ~95-98%

### Passive Attack Detector
- **Algorithm:** Gradient Boosting Classifier
- **Features:** 8 behavioral vectors
- **Expected Accuracy:** ~92-96%
- **ROC-AUC Score:** ~0.95+

## 🔍 Detection Output

### Threat Levels
- **LOW:** No threats detected
- **MEDIUM:** Passive attack detected
- **HIGH:** Active attack detected
- **CRITICAL:** Both attacks detected

### Example Output

```
======================================================================
COMPREHENSIVE SECURITY ANALYSIS
======================================================================

⏰ Timestamp: 2026-05-08T14:30:00
🎯 Overall Status: CRITICAL - BOTH ATTACKS DETECTED
⚠️  Threat Level: CRITICAL

----------------------------------------------------------------------
ACTIVE ATTACK DETECTION (File Tampering)
----------------------------------------------------------------------
File: data/tampered/document.pdf_flip
Status: TAMPERED
Tamper Probability: 98.50%

----------------------------------------------------------------------
PASSIVE ATTACK DETECTION (Behavioral Analysis)
----------------------------------------------------------------------
Status: PASSIVE ATTACK
Attack Probability: 94.20%
Risk Level: HIGH

----------------------------------------------------------------------
RECOMMENDATIONS
----------------------------------------------------------------------
  🚨 File integrity compromised - Do not use this file
  🔒 Verify file source and obtain clean copy
  ⚠️  Suspicious behavioral pattern detected (Risk: HIGH)
  🛡️  Monitor system for unauthorized access
  📊 Abnormally high read rate - possible timing attack
  💾 High cache miss rate - possible cache side-channel attack
======================================================================
```

## 📝 Logging

All detection results are automatically logged to `logs/detection_log_YYYYMMDD.json` with:
- Timestamp
- Detection results (active + passive)
- Threat level
- Recommendations

## 🔧 Customization

### Adjust Detection Thresholds

Edit `ml/passive_attack_detector.py`:

```python
# Risk level thresholds
if attack_probability < 0.3:
    risk_level = "LOW"
elif attack_probability < 0.7:
    risk_level = "MEDIUM"
else:
    risk_level = "HIGH"
```

### Add New Behavioral Features

1. Add feature to `FEATURE_NAMES` in `passive_attack_detector.py`
2. Update data generation in `passive_data_generator.py`
3. Retrain model

### Modify Attack Patterns

Edit `passive_data_generator.py` to adjust attack characteristics:

```python
# Example: More aggressive timing attack
'read_ops_per_sec': round(random.uniform(200, 500), 2),  # Increased
'decrypt_calls': random.randint(500, 2000),  # More attempts
```

## 🛡️ Security Best Practices

1. **Regular Model Updates:** Retrain models with new attack patterns
2. **Threshold Tuning:** Adjust based on false positive/negative rates
3. **Multi-Layer Defense:** Use both active and passive detection
4. **Log Analysis:** Review detection logs regularly
5. **Incident Response:** Have procedures for detected attacks

## 📚 Technical Details

### Active Attack Features
1. **File Size:** Detects truncation/padding
2. **Entropy:** Measures randomness (tampering changes entropy)
3. **Byte Mean/Std:** Statistical distribution changes
4. **Format Validation:** PDF/JPG header checks

### Passive Attack Features
1. **Read Operations:** Frequency analysis
2. **Block Size:** Access pattern analysis
3. **Session Duration:** Temporal analysis
4. **Decrypt Calls:** Cryptographic operation monitoring
5. **Sequence Entropy:** Access randomness
6. **Cache Behavior:** Side-channel detection
7. **Reopen Patterns:** Probing detection
8. **Timing Analysis:** Statistical anomaly detection

## 🤝 Contributing

To add new attack types:
1. Update data generators with new patterns
2. Retrain models
3. Update documentation
4. Test thoroughly

## 📄 License

[Your License Here]

## 🆘 Troubleshooting

### Model Not Found Error
```bash
# Run training first
python -c "from ml.train_model import train_model; train_model()"
python -c "from ml.passive_attack_detector import train_passive_detector; train_passive_detector()"
```

### Dataset Not Found Error
```bash
# Generate datasets first
python tempered_generator.py
python passive_data_generator.py
```

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt
```

## 📞 Support

For issues or questions, please check:
1. System status (Option 9 in menu)
2. Log files in `logs/` directory
3. Model files in `models/` directory

---

**Built with:** Python, scikit-learn, NumPy, PyCryptodome
**Version:** 1.0.0
**Last Updated:** May 2026
