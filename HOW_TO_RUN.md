# How to Run the Attack Detection System

## � Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Windows OS (you're already on Windows)

## 🚀 Step-by-Step Instructions

### Step 1: Install Dependencies

Open Command Prompt or PowerShell in the project directory and run:

```bash
pip install -r requirements.txt
```

**What this installs:**
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning library
- `pycryptodome` - Cryptography library
- `pandas` - Data processing (optional)
- `matplotlib` & `seaborn` - Visualization (optional)

**If you get errors, try:**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 2: Choose Your Method

You have **3 ways** to run the system:

## 🎯 METHOD 1: Quick Demo (Recommended for First Time)

**Best for:** Seeing examples and understanding how it works

```bash
python demo.py
```

**What it does:**
- Shows examples of passive attack detection
- Shows examples of active attack detection
- Demonstrates unified detection
- Interactive menu to explore

**Menu Options:**
```
1. Demo Passive Attack Detection
2. Demo Active Attack Detection
3. Demo Unified Detection (Both)
4. Run All Demos
0. Exit
```

---

## 🎯 METHOD 2: Interactive Menu System (Recommended for Full Control)

**Best for:** Complete control over all operations

```bash
python run_complete_system.py
```

**Menu Options:**
```
1. Generate Active Attack Dataset (tampered files)
2. Generate Passive Attack Dataset (behavioral data)
3. Train Active Attack Detector
4. Train Passive Attack Detector
5. Test Active Attack Detection
6. Test Passive Attack Detection
7. Run Unified Detection (Both Active + Passive)
8. Run Complete Pipeline (Generate + Train + Test)  ← START HERE
9. View System Status
0. Exit
```

**First Time Users:** Select option **8** to run everything automatically!

---

## 🎯 METHOD 3: Direct Python API

**Best for:** Integrating into your own code

### Detect Passive Attacks (Behavioral)

```python
from ml.passive_attack_detector import detect_passive_attack

# Example: Normal behavior
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

result = detect_passive_attack(normal_behavior)
print(f"Prediction: {result['prediction']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Attack Probability: {result['attack_probability']:.2%}")
```

### Detect Active Attacks (File Tampering)

```python
from ml.detect_tamper import detect_tampering

# Check if a file has been tampered
result = detect_tampering("data/original/document.pdf")
print(result)  # "✅ File is SAFE" or "❌ File is TAMPERED"
```

### Unified Detection (Both)

```python
from ml.unified_attack_detector import UnifiedAttackDetector

detector = UnifiedAttackDetector()

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

print(f"Overall Status: {result['overall_status']}")
print(f"Threat Level: {result['threat_level']}")
```

---

## 🎨 BONUS: Visualize Attack Patterns

```bash
python visualize_attacks.py
```

**What it shows:**
- Comparison of normal vs attack behaviors
- Attack type characteristics
- Detection thresholds
- ASCII bar charts

---

## 📝 Complete Workflow Example

### First Time Setup (Do Once)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the complete pipeline
python run_complete_system.py
# Then select: 8 (Run Complete Pipeline)
```

This will:
1. ✅ Generate active attack dataset (tampered files)
2. ✅ Generate passive attack dataset (behavioral data)
3. ✅ Train active attack detector
4. ✅ Train passive attack detector
5. ✅ Test both detectors
6. ✅ Show results

**Time:** ~30 seconds

---

### After Setup - Testing

```bash
# Quick demo
python demo.py

# Or use the menu
python run_complete_system.py
# Select option 7: Run Unified Detection
```

---

## � What Each Script Does

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `demo.py` | Interactive demonstrations | First time, learning |
| `run_complete_system.py` | Full menu system | Complete control |
| `visualize_attacks.py` | Pattern visualization | Understanding attacks |
| `passive_data_generator.py` | Generate behavioral data | Manual data generation |
| `tempered_generator.py` | Generate tampered files | Manual data generation |

---

## 🎯 Quick Commands Reference

### Generate Data
```bash
# Generate passive attack data
python passive_data_generator.py

# Generate active attack data (tampered files)
python tempered_generator.py
```

### Train Models
```bash
# Train passive attack detector
python -c "from ml.passive_attack_detector import train_passive_detector; train_passive_detector()"

# Train active attack detector
python -c "from ml.train_model import train_model; train_model()"
```

### Test Models
```bash
# Test passive detector
python -c "from ml.passive_attack_detector import test_passive_detector; test_passive_detector()"

# Test active detector
python -c "from ml.detect_tamper import detect_tampering; print(detect_tampering('data/original/cryptography_ml_ideas.pdf'))"
```

---

## 🐛 Troubleshooting

### Problem 1: "No module named 'sklearn'"
**Solution:**
```bash
pip install scikit-learn
```

### Problem 2: "No module named 'Crypto'"
**Solution:**
```bash
pip install pycryptodome
```

### Problem 3: "Model not found"
**Solution:** Train the models first
```bash
python run_complete_system.py
# Select option 8: Run Complete Pipeline
```

### Problem 4: "Dataset not found"
**Solution:** Generate datasets first
```bash
python passive_data_generator.py
python tempered_generator.py
```

### Problem 5: Import errors in scripts
**Solution:** Make sure you're in the correct directory
```bash
cd e:\crypto-ml\crypto-ml
python demo.py
```

---

## 📊 Expected Output Examples

### When Running Demo
```
============================================================
PASSIVE ATTACK DETECTION DEMO
============================================================

────────────────────────────────────────────────────────────
Scenario: ✅ Normal User Behavior
────────────────────────────────────────────────────────────
  Read Ops/sec: 12.5
  Block Size: 8192 bytes
  Decrypt Calls: 5
  Cache Miss Rate: 12.00%
  Access Time Z-Score: 0.50

  🔍 Detection Result:
     Status: NORMAL BEHAVIOR
     Attack Probability: 0.00%
     Risk Level: LOW
     ✅ SAFE
```

### When Running Unified Detection
```
======================================================================
COMPREHENSIVE SECURITY ANALYSIS
======================================================================

⏰ Timestamp: 2026-05-08T15:30:00
🎯 Overall Status: SECURE - NO THREATS DETECTED
⚠️  Threat Level: LOW

----------------------------------------------------------------------
ACTIVE ATTACK DETECTION (File Tampering)
----------------------------------------------------------------------
File: data/original/document.pdf
Status: SAFE
Tamper Probability: 2.50%

----------------------------------------------------------------------
PASSIVE ATTACK DETECTION (Behavioral Analysis)
----------------------------------------------------------------------
Status: NORMAL
Attack Probability: 0.01%
Risk Level: LOW

----------------------------------------------------------------------
RECOMMENDATIONS
----------------------------------------------------------------------
  ✅ System appears secure
  ✅ Continue normal operations
======================================================================
```

---

## 🎓 Learning Path

### Beginner (5 minutes)
```bash
python demo.py
# Select option 4: Run All Demos
```

### Intermediate (10 minutes)
```bash
python run_complete_system.py
# Select option 8: Run Complete Pipeline
# Then explore other options
```

### Advanced (30 minutes)
1. Read `ATTACK_COMPARISON.md`
2. Run `python visualize_attacks.py`
3. Modify detection thresholds
4. Test with custom data

---

## 💡 Pro Tips

1. **First time?** Run `python demo.py` to see examples
2. **Want full control?** Use `python run_complete_system.py`
3. **Need to retrain?** Option 8 in the menu does everything
4. **Check status?** Option 9 shows what's installed
5. **Understand attacks?** Run `python visualize_attacks.py`

---

## 📞 Quick Help

**Command not working?**
- Make sure you're in the right directory: `cd e:\crypto-ml\crypto-ml`
- Check Python is installed: `python --version`
- Check pip is installed: `pip --version`

**Still stuck?**
- Check `QUICK_START.md` for quick reference
- Check `SYSTEM_SUMMARY.md` for system overview
- Check `INDEX.md` for complete navigation

---

## 🚀 Recommended First Run

```bash
# Step 1: Install
pip install -r requirements.txt

# Step 2: Run demo
python demo.py

# Step 3: Explore menu
python run_complete_system.py
```

**That's it!** You're ready to detect attacks! 🎉
