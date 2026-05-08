# Quick Start Guide - Attack Detection System

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Datasets
```bash
# Generate active attack data (tampered files)
python tempered_generator.py

# Generate passive attack data (behavioral patterns)
python passive_data_generator.py
```

### Step 3: Train Models
```bash
# Train both models
python -c "from ml.train_model import train_model; train_model()"
python -c "from ml.passive_attack_detector import train_passive_detector; train_passive_detector()"
```

### Step 4: Run Demo
```bash
python demo.py
```

## 📋 Quick Commands

### Interactive Menu System
```bash
python run_complete_system.py
```
This provides a full menu with all options.

### One-Command Setup
```bash
# Run everything at once (from menu option 8)
python run_complete_system.py
# Then select: 8 (Run Complete Pipeline)
```

## 🎯 Quick Tests

### Test Active Attack Detection
```python
from ml.detect_tamper import detect_tampering

# Test a file
result = detect_tampering("data/original/document.pdf")
print(result)  # ✅ File is SAFE

result = detect_tampering("data/tampered/document.pdf_flip")
print(result)  # ❌ File is TAMPERED
```

### Test Passive Attack Detection
```python
from ml.passive_attack_detector import detect_passive_attack

# Normal behavior
normal = {
    'read_ops_per_sec': 12.5,
    'avg_read_block_size': 8192,
    'session_duration': 300.0,
    'decrypt_calls': 5,
    'entropy_of_read_sequence': 0.75,
    'cache_miss_rate': 0.12,
    'reopen_frequency': 1,
    'access_time_zscore': 0.5
}
result = detect_passive_attack(normal)
print(result['prediction'])  # NORMAL BEHAVIOR

# Attack behavior
attack = {
    'read_ops_per_sec': 180.0,
    'avg_read_block_size': 256,
    'session_duration': 20.0,
    'decrypt_calls': 350,
    'entropy_of_read_sequence': 0.28,
    'cache_miss_rate': 0.78,
    'reopen_frequency': 45,
    'access_time_zscore': 5.2
}
result = detect_passive_attack(attack)
print(result['prediction'])  # PASSIVE ATTACK DETECTED
print(result['risk_level'])  # HIGH
```

### Test Unified Detection
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

print(result['overall_status'])
print(result['threat_level'])
```

## 📊 Understanding the Output

### Active Detection Output
- `✅ File is SAFE` - No tampering detected
- `❌ File is TAMPERED` - File has been modified

### Passive Detection Output
```python
{
    'prediction': 'PASSIVE ATTACK DETECTED',
    'attack_probability': 0.94,
    'risk_level': 'HIGH',
    'is_attack': True
}
```

### Unified Detection Output
```
Overall Status: CRITICAL - BOTH ATTACKS DETECTED
Threat Level: CRITICAL

RECOMMENDATIONS:
  🚨 File integrity compromised - Do not use this file
  ⚠️  Suspicious behavioral pattern detected (Risk: HIGH)
  🛡️  Monitor system for unauthorized access
```

## 🔧 Troubleshooting

### "Model not found" Error
```bash
# Train the models first
python -c "from ml.train_model import train_model; train_model()"
python -c "from ml.passive_attack_detector import train_passive_detector; train_passive_detector()"
```

### "Dataset not found" Error
```bash
# Generate datasets first
python tempered_generator.py
python passive_data_generator.py
```

### Import Errors
```bash
# Install dependencies
pip install numpy scikit-learn pycryptodome
```

## 📁 File Structure Quick Reference

```
crypto-ml/
├── data/
│   ├── original/              # Clean files
│   ├── tampered/              # Tampered files (active attacks)
│   └── passive_attacks/       # Behavioral data (passive attacks)
├── ml/
│   ├── passive_attack_detector.py   # Passive detection
│   ├── detect_tamper.py             # Active detection
│   └── unified_attack_detector.py   # Both combined
├── models/
│   ├── tamper_model.pkl             # Active model
│   └── passive_attack_model.pkl     # Passive model
├── run_complete_system.py           # Main menu
└── demo.py                          # Interactive demo
```

## 🎓 Learning Path

1. **Start Here:** Run `python demo.py` to see examples
2. **Understand:** Read `ATTACK_COMPARISON.md` for theory
3. **Deep Dive:** Read `README_ATTACK_DETECTION.md` for details
4. **Customize:** Modify detection thresholds and features

## 💡 Common Use Cases

### Use Case 1: File Integrity Check
```python
from ml.detect_tamper import detect_tampering
result = detect_tampering("important_file.pdf")
```

### Use Case 2: Monitor User Behavior
```python
from ml.passive_attack_detector import detect_passive_attack

# Collect metrics during file access
metrics = collect_access_metrics()  # Your implementation
result = detect_passive_attack(metrics)

if result['is_attack']:
    alert_security_team(result)
```

### Use Case 3: Comprehensive Security Check
```python
from ml.unified_attack_detector import UnifiedAttackDetector

detector = UnifiedAttackDetector()

# Check both file and behavior
result = detector.comprehensive_check(file_path, behavior_data)

if result['threat_level'] in ['HIGH', 'CRITICAL']:
    block_access()
    log_incident(result)
```

## 📞 Next Steps

- ✅ Run the demo: `python demo.py`
- ✅ Read the comparison: `ATTACK_COMPARISON.md`
- ✅ Explore the full docs: `README_ATTACK_DETECTION.md`
- ✅ Customize for your needs

## 🎯 Key Takeaways

1. **Active Detection** = File tampering (static analysis)
2. **Passive Detection** = Behavioral anomalies (dynamic analysis)
3. **Unified Detection** = Both combined for maximum security
4. **8 Behavioral Vectors** = Comprehensive passive attack coverage
5. **Real-time Monitoring** = Detect attacks as they happen

---

**Ready to start?** Run: `python demo.py`
