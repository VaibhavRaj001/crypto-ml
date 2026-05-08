"""
Visualization of Attack Patterns
Shows the difference between normal and attack behaviors
"""
import json
import os

def load_passive_data():
    """Load passive attack data"""
    normal_path = "data/passive_attacks/normal_behavior.json"
    attack_path = "data/passive_attacks/passive_attacks.json"
    
    if not os.path.exists(normal_path) or not os.path.exists(attack_path):
        print("❌ Data files not found. Run passive_data_generator.py first.")
        return None, None
    
    with open(normal_path, 'r') as f:
        normal_data = json.load(f)
    
    with open(attack_path, 'r') as f:
        attack_data = json.load(f)
    
    return normal_data, attack_data


def calculate_stats(data, feature):
    """Calculate statistics for a feature"""
    values = [record[feature] for record in data]
    return {
        'min': min(values),
        'max': max(values),
        'avg': sum(values) / len(values),
        'count': len(values)
    }


def create_ascii_bar(value, max_value, width=40):
    """Create ASCII bar chart"""
    filled = int((value / max_value) * width)
    bar = '█' * filled + '░' * (width - filled)
    return bar


def visualize_comparison():
    """Visualize normal vs attack patterns"""
    print("\n" + "=" * 80)
    print("BEHAVIORAL PATTERN COMPARISON")
    print("=" * 80)
    
    normal_data, attack_data = load_passive_data()
    
    if normal_data is None:
        return
    
    features = [
        ('read_ops_per_sec', 'Read Operations/Sec'),
        ('avg_read_block_size', 'Avg Block Size (bytes)'),
        ('session_duration', 'Session Duration (sec)'),
        ('decrypt_calls', 'Decrypt Calls'),
        ('entropy_of_read_sequence', 'Sequence Entropy'),
        ('cache_miss_rate', 'Cache Miss Rate'),
        ('reopen_frequency', 'Reopen Frequency'),
        ('access_time_zscore', 'Access Time Z-Score')
    ]
    
    for feature, label in features:
        normal_stats = calculate_stats(normal_data, feature)
        attack_stats = calculate_stats(attack_data, feature)
        
        print(f"\n{'─' * 80}")
        print(f"📊 {label}")
        print('─' * 80)
        
        # Determine max for scaling
        max_val = max(normal_stats['max'], attack_stats['max'])
        
        # Normal behavior
        print(f"\n✅ NORMAL BEHAVIOR:")
        print(f"   Range: {normal_stats['min']:.2f} - {normal_stats['max']:.2f}")
        print(f"   Average: {normal_stats['avg']:.2f}")
        bar = create_ascii_bar(normal_stats['avg'], max_val)
        print(f"   {bar} {normal_stats['avg']:.2f}")
        
        # Attack behavior
        print(f"\n🚨 ATTACK BEHAVIOR:")
        print(f"   Range: {attack_stats['min']:.2f} - {attack_stats['max']:.2f}")
        print(f"   Average: {attack_stats['avg']:.2f}")
        bar = create_ascii_bar(attack_stats['avg'], max_val)
        print(f"   {bar} {attack_stats['avg']:.2f}")
        
        # Difference
        diff_percent = ((attack_stats['avg'] - normal_stats['avg']) / normal_stats['avg'] * 100)
        if abs(diff_percent) > 10:
            indicator = "⚠️  SIGNIFICANT DIFFERENCE"
        else:
            indicator = "ℹ️  Similar"
        print(f"\n   Difference: {diff_percent:+.1f}% {indicator}")


def show_attack_types():
    """Show characteristics of different attack types"""
    print("\n" + "=" * 80)
    print("ATTACK TYPE CHARACTERISTICS")
    print("=" * 80)
    
    attack_types = {
        '⏱️  Timing Attack': {
            'description': 'Measures operation times to extract cryptographic keys',
            'characteristics': [
                'Very high read rate (50-200 ops/sec)',
                'Small block sizes (64-512 bytes)',
                'Short bursts (10-60 seconds)',
                'Many decrypt attempts (50-500)',
                'Low entropy - repetitive pattern',
                'High cache miss rate',
                'Frequent file reopens',
                'Anomalous timing (z-score > 2.5)'
            ]
        },
        '💾 Cache Attack': {
            'description': 'Analyzes cache behavior to leak information',
            'characteristics': [
                'Extremely high read rate (100-300 ops/sec)',
                'Cache line sized blocks (32-256 bytes)',
                'Quick probing sessions (5-30 seconds)',
                'Massive decrypt attempts (100-1000)',
                'Very low entropy - systematic scanning',
                'Very high cache miss rate (60-90%)',
                'Very frequent reopens (20-100)',
                'Highly anomalous timing (z-score > 3.0)'
            ]
        },
        '⚡ Power Analysis': {
            'description': 'Monitors power consumption during crypto operations',
            'characteristics': [
                'Moderate-high read rate (30-80 ops/sec)',
                'Varied block sizes (128-1024 bytes)',
                'Long monitoring sessions (2-30 minutes)',
                'Many decrypt operations (200-2000)',
                'Low entropy - controlled patterns',
                'Moderate-high cache misses (30-60%)',
                'Some file reopens (5-20)',
                'Anomalous timing (z-score > 2.0)'
            ]
        },
        '🗂️  Memory Dump': {
            'description': 'Attempts to dump memory contents',
            'characteristics': [
                'Extremely high read rate (150-500 ops/sec)',
                'Large block sizes (8K-64K bytes)',
                'Very short sessions (2-20 seconds)',
                'Few decrypt calls (1-5)',
                'High entropy - scanning memory',
                'Very high cache misses (70-95%)',
                'Minimal reopens (0-2)',
                'Extremely anomalous timing (z-score > 4.0)'
            ]
        }
    }
    
    for attack_name, info in attack_types.items():
        print(f"\n{'─' * 80}")
        print(f"{attack_name}")
        print('─' * 80)
        print(f"Description: {info['description']}")
        print(f"\nCharacteristics:")
        for char in info['characteristics']:
            print(f"  • {char}")


def show_detection_thresholds():
    """Show detection thresholds"""
    print("\n" + "=" * 80)
    print("DETECTION THRESHOLDS")
    print("=" * 80)
    
    thresholds = [
        {
            'vector': 'Read Ops/Sec',
            'normal': '5-20',
            'suspicious': '20-50',
            'attack': '>50',
            'critical': '>100'
        },
        {
            'vector': 'Block Size',
            'normal': '4K-16K',
            'suspicious': '512-4K',
            'attack': '<512',
            'critical': '<128'
        },
        {
            'vector': 'Session Duration',
            'normal': '60-600s',
            'suspicious': '30-60s',
            'attack': '<30s',
            'critical': '<10s'
        },
        {
            'vector': 'Decrypt Calls',
            'normal': '1-10',
            'suspicious': '10-50',
            'attack': '>50',
            'critical': '>200'
        },
        {
            'vector': 'Sequence Entropy',
            'normal': '0.6-0.85',
            'suspicious': '0.4-0.6',
            'attack': '<0.4',
            'critical': '<0.25'
        },
        {
            'vector': 'Cache Miss Rate',
            'normal': '5-20%',
            'suspicious': '20-40%',
            'attack': '>40%',
            'critical': '>70%'
        },
        {
            'vector': 'Reopen Frequency',
            'normal': '0-3',
            'suspicious': '3-10',
            'attack': '>10',
            'critical': '>30'
        },
        {
            'vector': 'Access Time Z-Score',
            'normal': '-1.5 to 1.5',
            'suspicious': '1.5-2.5',
            'attack': '>2.5',
            'critical': '>4.0'
        }
    ]
    
    print(f"\n{'Vector':<25} {'Normal':<15} {'Suspicious':<15} {'Attack':<15} {'Critical':<15}")
    print('─' * 85)
    
    for t in thresholds:
        print(f"{t['vector']:<25} {t['normal']:<15} {t['suspicious']:<15} {t['attack']:<15} {t['critical']:<15}")


def main():
    """Main visualization function"""
    print("\n" + "=" * 80)
    print("ATTACK PATTERN VISUALIZATION TOOL")
    print("=" * 80)
    
    while True:
        print("\n📊 VISUALIZATION MENU")
        print("─" * 80)
        print("1. Compare Normal vs Attack Patterns")
        print("2. Show Attack Type Characteristics")
        print("3. Show Detection Thresholds")
        print("4. Show All")
        print("0. Exit")
        print("─" * 80)
        
        choice = input("\nSelect option (0-4): ").strip()
        
        if choice == '1':
            visualize_comparison()
        elif choice == '2':
            show_attack_types()
        elif choice == '3':
            show_detection_thresholds()
        elif choice == '4':
            visualize_comparison()
            show_attack_types()
            show_detection_thresholds()
        elif choice == '0':
            print("\n👋 Exiting visualization tool.")
            break
        else:
            print("\n❌ Invalid choice. Please enter 0-4.")
        
        if choice in ['1', '2', '3', '4']:
            input("\n⏸️  Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted. Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
