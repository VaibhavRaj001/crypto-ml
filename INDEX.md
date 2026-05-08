# Cryptography + ML Attack Detection System - Complete Index

## 🚀 Quick Navigation

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - Get up and running in 5 minutes
- **[SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)** - System overview and status
- **[README_ATTACK_DETECTION.md](README_ATTACK_DETECTION.md)** - Complete documentation

### Understanding the System
- **[ATTACK_COMPARISON.md](ATTACK_COMPARISON.md)** - Active vs Passive attacks explained
- **[INDEX.md](INDEX.md)** - This file - complete navigation

## 📁 File Organization

### 🎮 User Interfaces
| File | Purpose | When to Use |
|------|---------|-------------|
| `run_complete_system.py` | Interactive menu system | Main interface for all operations |
| `demo.py` | Quick demonstrations | See examples of detection in action |
| `visualize_attacks.py` | Pattern visualization | Understand attack characteristics |

### 🤖 Core Detection Modules
| File | Purpose | API |
|------|---------|-----|
| `ml/passive_attack_detector.py` | Passive attack detection | `detect_passive_attack(behavioral_data)` |
| `ml/detect_tamper.py` | Active attack detection | `detect_tampering(file_path)` |
| `ml/unified_attack_detector.py` | Combined detection | `UnifiedAttackDetector().comprehensive_check()` |
| `ml/feature_extraction.py` | File feature extraction | `extract_features(file_path)` |
| `ml/train_model.py` | Active model training | `train_model()` |

### 🔧 Data Generation
| File | Purpose | Output |
|------|---------|--------|
| `passive_data_generator.py` | Generate behavioral data | `data/passive_attacks/*.json` |
| `tempered_generator.py` | Generate tampered files | `data/tampered/*` |

### 📊 Data Directories
```
data/
├── original/              # Clean files (14 files)
├── tampered/              # Tampered files (56 files)
└── passive_attacks/       # Behavioral data (JSON)
    ├── passive_train.json      # Training data (1000 samples)
    ├── passive_test.json       # Test data (200 samples)
    ├── normal_behavior.json    # Normal patterns (500 samples)
    └── passive_attacks.json    # Attack patterns (500 samples)
```

### 🤖 Model Files
```
models/
├── tamper_model.pkl           # Active attack detector
└── passive_attack_model.pkl   # Passive attack detector
```

### 📝 Documentation
| File | Content |
|------|---------|
| `README_ATTACK_DETECTION.md` | Complete system documentation |
| `QUICK_START.md` | Quick start guide |
| `SYSTEM_SUMMARY.md` | System status and summary |
| `ATTACK_COMPARISON.md` | Active vs Passive comparison |
| `INDEX.md` | This navigation file |

## 🎯 Common Tasks

### Task 1: First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run complete pipeline
python run_complete_system.py
# Select option 8: Run Complete Pipeline
```

### Task 2: Test the System
```bash
# Interactive demo
python demo.py
```

### Task 3: Detect Active Attack
```python
from ml.detect_tamper import detect_tampering
result = detect_tampering("path/to/file.pdf")
print(result)
```

### Task 4: Detect Passive Attack
```python
from ml.passive_attack_detector import detect_passive_attack

behavioral_data = {
    'read_ops_per_sec': 12.5,
    'avg_read_block_size': 8192,
    'session_duration': 300.0,
    'decrypt_calls': 5,
    'entropy_of_read_sequence': 0.75,
    'cache_miss_rate': 0.12,
    'reopen_frequency': 1,
    'access_time_zscore': 0.5
}

result = detect_passive_attack(behavioral_data)
print(result)
```

### Task 5: Unified Detection
```python
from ml.unified_attack_detector import UnifiedAttackDetector

detector = UnifiedAttackDetector()
result = detector.comprehensive_check(file_path, behavioral_data)
print(result['overall_status'])
```

### Task 6: Visualize Patterns
```bash
python visualize_attacks.py
```

### Task 7: Retrain Models
```bash
# After adding more data
python -c "from ml.train_model import train_model; train_model()"
python -c "from ml.passive_attack_detector import train_passive_detector; train_passive_detector()"
```

## 📚 Learning Path

### Beginner
1. Read **[QUICK_START.md](QUICK_START.md)**
2. Run `python demo.py`
3. Read **[SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)**

### Intermediate
1. Read **[ATTACK_COMPARISON.md](ATTACK_COMPARISON.md)**
2. Run `python visualize_attacks.py`
3. Experiment with `run_complete_system.py`

### Advanced
1. Read **[README_ATTACK_DETECTION.md](README_ATTACK_DETECTION.md)**
2. Modify detection thresholds
3. Add custom attack patterns
4. Integrate into your application

## 🔍 Key Concepts

### Active Attacks (File Tampering)
- **What:** Direct modification of encrypted files
- **Detection:** File property analysis (6 features)
- **Examples:** Byte flipping, truncation, noise injection
- **Module:** `ml/detect_tamper.py`

### Passive Attacks (Behavioral)
- **What:** Observation-based attacks (eavesdropping)
- **Detection:** Behavioral analysis (8 vectors)
- **Examples:** Timing attacks, cache attacks, power analysis
- **Module:** `ml/passive_attack_detector.py`

### The 8 Behavioral Vectors
1. **read_ops_per_sec** - Operation frequency
2. **avg_read_block_size** - Access granularity
3. **session_duration** - Time duration
4. **decrypt_calls** - Crypto operations
5. **entropy_of_read_sequence** - Pattern randomness
6. **cache_miss_rate** - Cache behavior
7. **reopen_frequency** - File reopening
8. **access_time_zscore** - Timing anomalies

## 🎓 Use Cases

### Use Case 1: File Integrity Verification
```python
# Check if a file has been tampered with
from ml.detect_tamper import detect_tampering
result = detect_tampering("important_document.pdf")
```

### Use Case 2: Real-Time Monitoring
```python
# Monitor user behavior during file access
from ml.passive_attack_detector import detect_passive_attack

def monitor_file_access(user_session):
    metrics = collect_metrics(user_session)
    result = detect_passive_attack(metrics)
    
    if result['is_attack']:
        alert_security_team(result)
```

### Use Case 3: Comprehensive Security Check
```python
# Check both file and behavior
from ml.unified_attack_detector import UnifiedAttackDetector

detector = UnifiedAttackDetector()
result = detector.comprehensive_check(file_path, behavior_data)

if result['threat_level'] in ['HIGH', 'CRITICAL']:
    block_access()
```

## 🛠️ Customization Guide

### Adjust Detection Sensitivity
**File:** `ml/passive_attack_detector.py`
```python
# Line ~120: Adjust risk thresholds
if attack_probability < 0.3:    # Increase for fewer alerts
    risk_level = "LOW"
elif attack_probability < 0.7:  # Adjust middle range
    risk_level = "MEDIUM"
else:
    risk_level = "HIGH"
```

### Add New Attack Patterns
**File:** `passive_data_generator.py`
```python
# Add new attack type in generate_passive_attack_behavior()
elif attack_type == 'new_attack':
    record = {
        'session_id': f'new_attack_{i}',
        'read_ops_per_sec': ...,
        # Define characteristics
    }
```

### Modify Model Parameters
**File:** `ml/passive_attack_detector.py`
```python
# Line ~80: Adjust model parameters
model = GradientBoostingClassifier(
    n_estimators=200,      # More = better accuracy, slower
    learning_rate=0.1,     # Lower = more conservative
    max_depth=5            # Deeper = more complex patterns
)
```

## 📊 System Performance

### Passive Attack Detection
- **Accuracy:** 100% (on test set)
- **ROC-AUC:** 1.0000
- **Precision:** 100%
- **Recall:** 100%

### Active Attack Detection
- **Algorithm:** Random Forest
- **Features:** 6 file-based vectors
- **Training samples:** 70

### Most Important Features (Passive)
1. access_time_zscore (43.27%)
2. cache_miss_rate (37.11%)
3. read_ops_per_sec (19.61%)

## 🔧 Troubleshooting

### Problem: Model not found
**Solution:**
```bash
python -c "from ml.train_model import train_model; train_model()"
python -c "from ml.passive_attack_detector import train_passive_detector; train_passive_detector()"
```

### Problem: Dataset not found
**Solution:**
```bash
python tempered_generator.py
python passive_data_generator.py
```

### Problem: Import errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Low accuracy
**Solution:**
- Add more training data
- Adjust model parameters
- Check feature quality

## 📞 Quick Reference

### Command Cheat Sheet
```bash
# Setup
pip install -r requirements.txt

# Generate data
python tempered_generator.py
python passive_data_generator.py

# Train models
python -c "from ml.train_model import train_model; train_model()"
python -c "from ml.passive_attack_detector import train_passive_detector; train_passive_detector()"

# Run system
python run_complete_system.py  # Interactive menu
python demo.py                 # Quick demo
python visualize_attacks.py    # Visualizations

# Check status
python run_complete_system.py  # Option 9
```

### API Cheat Sheet
```python
# Active detection
from ml.detect_tamper import detect_tampering
detect_tampering(file_path)

# Passive detection
from ml.passive_attack_detector import detect_passive_attack
detect_passive_attack(behavioral_data)

# Unified detection
from ml.unified_attack_detector import UnifiedAttackDetector
detector = UnifiedAttackDetector()
detector.comprehensive_check(file_path, behavioral_data)
```

## 🎯 Project Structure Summary

```
crypto-ml/
├── 📄 Documentation
│   ├── INDEX.md                    # This file
│   ├── QUICK_START.md              # Quick start
│   ├── SYSTEM_SUMMARY.md           # System overview
│   ├── README_ATTACK_DETECTION.md  # Complete docs
│   └── ATTACK_COMPARISON.md        # Attack comparison
│
├── 🎮 User Interfaces
│   ├── run_complete_system.py      # Main menu
│   ├── demo.py                     # Demonstrations
│   └── visualize_attacks.py        # Visualizations
│
├── 🤖 ML Modules
│   └── ml/
│       ├── passive_attack_detector.py   # Passive detection
│       ├── detect_tamper.py             # Active detection
│       ├── unified_attack_detector.py   # Combined
│       ├── feature_extraction.py        # Features
│       └── train_model.py               # Training
│
├── 🔧 Data Generation
│   ├── passive_data_generator.py   # Behavioral data
│   └── tempered_generator.py       # Tampered files
│
├── 📊 Data & Models
│   ├── data/                       # Datasets
│   ├── models/                     # Trained models
│   └── logs/                       # Detection logs
│
└── ⚙️ Configuration
    └── requirements.txt            # Dependencies
```

## 🚀 Next Steps

1. **Start Here:** [QUICK_START.md](QUICK_START.md)
2. **Understand:** [ATTACK_COMPARISON.md](ATTACK_COMPARISON.md)
3. **Deep Dive:** [README_ATTACK_DETECTION.md](README_ATTACK_DETECTION.md)
4. **Experiment:** Run `python demo.py`
5. **Customize:** Modify thresholds and patterns
6. **Integrate:** Use in your application

---

**Need help?** Check the documentation files or run `python run_complete_system.py` for the interactive menu.

**Ready to start?** Run: `python demo.py`
