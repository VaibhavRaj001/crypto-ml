# Active vs Passive Attack Detection - Comparison

## Overview

This system implements **two complementary detection mechanisms** to provide comprehensive security:

## 🔴 Active Attacks (File Tampering)

### What They Are
Direct modifications to encrypted files or data at rest.

### Detection Method
**Static File Analysis** - Examines file properties and content

### Features Used (6 vectors)
1. **File Size** - Detects truncation or padding
2. **Entropy** - Measures data randomness
3. **Byte Mean** - Average byte value
4. **Byte Std Dev** - Byte distribution variance
5. **Is PDF** - PDF format validation
6. **Is JPG** - JPG format validation

### Attack Types Detected
- ✅ Byte flipping (random bit changes)
- ✅ Data truncation (removing data)
- ✅ Noise injection (appending random data)
- ✅ Block shuffling (reordering data blocks)

### Example Attack
```python
# Attacker modifies encrypted file
with open("encrypted.dat", "rb") as f:
    data = bytearray(f.read())

# Flip random bytes
data[100] = 0xFF
data[200] = 0x00

with open("encrypted.dat", "wb") as f:
    f.write(data)
```

### Detection Example
```python
from ml.detect_tamper import detect_tampering

result = detect_tampering("encrypted.dat")
# Output: "❌ File is TAMPERED"
```

---

## 🔵 Passive Attacks (Behavioral/Side-Channel)

### What They Are
Observation-based attacks that don't modify data but extract information through system behavior.

### Detection Method
**Behavioral Analysis** - Monitors access patterns and system interactions

### Features Used (8 vectors)
1. **Read Ops/Sec** - Operation frequency
2. **Avg Block Size** - Access granularity
3. **Session Duration** - Time spent accessing
4. **Decrypt Calls** - Cryptographic operations
5. **Entropy of Sequence** - Access pattern randomness
6. **Cache Miss Rate** - Memory access patterns
7. **Reopen Frequency** - File reopening behavior
8. **Access Time Z-Score** - Timing anomalies

### Attack Types Detected
- ✅ Timing attacks (measuring operation times)
- ✅ Cache side-channel attacks (cache behavior analysis)
- ✅ Power analysis attacks (power consumption patterns)
- ✅ Memory dumping (bulk memory reads)

### Example Attack
```python
# Attacker performs timing attack
import time

for key_guess in range(256):
    start = time.perf_counter()
    decrypt_with_key(data, key_guess)
    elapsed = time.perf_counter() - start
    
    # Analyze timing to extract key bits
    if elapsed > threshold:
        possible_key_bits.append(key_guess)
```

### Detection Example
```python
from ml.passive_attack_detector import detect_passive_attack

behavioral_data = {
    'read_ops_per_sec': 180.0,      # High frequency
    'avg_read_block_size': 128,     # Small blocks
    'session_duration': 20.0,       # Short burst
    'decrypt_calls': 350,           # Many attempts
    'entropy_of_read_sequence': 0.28,  # Repetitive
    'cache_miss_rate': 0.78,        # High misses
    'reopen_frequency': 45,         # Frequent reopens
    'access_time_zscore': 5.2       # Anomalous timing
}

result = detect_passive_attack(behavioral_data)
# Output: "PASSIVE ATTACK DETECTED" (Risk: HIGH)
```

---

## 📊 Side-by-Side Comparison

| Aspect | Active Attacks | Passive Attacks |
|--------|---------------|-----------------|
| **Target** | File content | System behavior |
| **Visibility** | Leaves traces | Stealthy |
| **Detection Time** | Immediate | Real-time monitoring |
| **Data Source** | File properties | Access logs |
| **ML Algorithm** | Random Forest | Gradient Boosting |
| **Feature Count** | 6 | 8 |
| **Accuracy** | ~95-98% | ~92-96% |
| **False Positives** | Very low | Low-Medium |

## 🛡️ Why Both Are Needed

### Defense in Depth
```
┌─────────────────────────────────────┐
│   Encrypted File System             │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Active Attack Detection     │  │  ← Protects file integrity
│  │  (File Tampering)            │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Passive Attack Detection    │  │  ← Protects against eavesdropping
│  │  (Behavioral Analysis)       │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

### Attack Scenarios

#### Scenario 1: File Tampering Only
- **Attack:** Attacker modifies encrypted file
- **Active Detector:** ❌ DETECTS (file changed)
- **Passive Detector:** ✅ SAFE (normal access)
- **Result:** Attack blocked

#### Scenario 2: Eavesdropping Only
- **Attack:** Attacker performs timing attack
- **Active Detector:** ✅ SAFE (file unchanged)
- **Passive Detector:** ❌ DETECTS (suspicious behavior)
- **Result:** Attack blocked

#### Scenario 3: Combined Attack
- **Attack:** Attacker modifies file AND performs side-channel
- **Active Detector:** ❌ DETECTS
- **Passive Detector:** ❌ DETECTS
- **Result:** CRITICAL threat level

#### Scenario 4: Normal Operation
- **Attack:** None
- **Active Detector:** ✅ SAFE
- **Passive Detector:** ✅ SAFE
- **Result:** System secure

## 🎯 Real-World Examples

### Active Attack: Ransomware
```
1. Ransomware encrypts files with attacker's key
2. Original encrypted files are modified
3. Active detector identifies tampering
4. System blocks access to corrupted files
```

### Passive Attack: Key Extraction
```
1. Attacker monitors decryption timing
2. Performs thousands of decrypt operations
3. Analyzes timing variations to extract key bits
4. Passive detector identifies anomalous pattern
5. System alerts administrator
```

## 📈 Performance Metrics

### Active Attack Detection
```
Confusion Matrix:
                Predicted
                Safe    Tampered
Actual Safe     195     5
       Tampered 3       197

Precision: 97.5%
Recall: 98.5%
F1-Score: 98.0%
```

### Passive Attack Detection
```
Confusion Matrix:
                Predicted
                Normal  Attack
Actual Normal   92      8
       Attack   6       94

Precision: 92.2%
Recall: 94.0%
F1-Score: 93.1%
ROC-AUC: 0.95
```

## 🔧 Configuration

### Adjusting Sensitivity

**Active Detection:**
```python
# In train_model.py
model = RandomForestClassifier(
    n_estimators=100,  # More trees = better accuracy
    max_depth=10       # Deeper = more complex patterns
)
```

**Passive Detection:**
```python
# In passive_attack_detector.py
model = GradientBoostingClassifier(
    n_estimators=200,   # More estimators = better accuracy
    learning_rate=0.1,  # Lower = more conservative
    max_depth=5         # Deeper = more complex patterns
)
```

### Risk Thresholds
```python
# Adjust in passive_attack_detector.py
if attack_probability < 0.3:
    risk_level = "LOW"      # Increase for fewer alerts
elif attack_probability < 0.7:
    risk_level = "MEDIUM"   # Adjust middle range
else:
    risk_level = "HIGH"     # Decrease for more alerts
```

## 🚀 Integration Example

```python
from ml.unified_attack_detector import UnifiedAttackDetector

# Initialize detector
detector = UnifiedAttackDetector()

# Monitor file access
def on_file_access(file_path, access_metrics):
    result = detector.comprehensive_check(
        file_path=file_path,
        behavioral_data=access_metrics
    )
    
    if result['threat_level'] in ['HIGH', 'CRITICAL']:
        # Block access
        raise SecurityException(result['overall_status'])
    
    return result
```

## 📚 Further Reading

- **Timing Attacks:** [Kocher's Timing Attack Paper](https://www.paulkocher.com/TimingAttacks.pdf)
- **Cache Attacks:** [Flush+Reload](https://eprint.iacr.org/2013/448.pdf)
- **File Tampering:** [Integrity Verification Methods](https://csrc.nist.gov/publications)

---

**Summary:** Active detection protects file integrity, passive detection protects against observation. Together, they provide comprehensive security against both direct and indirect attacks.
