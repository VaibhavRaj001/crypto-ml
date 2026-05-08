"""
Quick Demo of the Attack Detection System
Shows both active and passive attack detection in action
"""
import os
import json

def print_banner(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def demo_passive_attacks():
    """Demonstrate passive attack detection with various scenarios"""
    from ml.passive_attack_detector import detect_passive_attack
    
    print_banner("PASSIVE ATTACK DETECTION DEMO")
    
    scenarios = [
        {
            'name': '✅ Normal User Behavior',
            'data': {
                'read_ops_per_sec': 12.5,
                'avg_read_block_size': 8192,
                'session_duration': 300.0,
                'decrypt_calls': 5,
                'entropy_of_read_sequence': 0.75,
                'cache_miss_rate': 0.12,
                'reopen_frequency': 1,
                'access_time_zscore': 0.5
            }
        },
        {
            'name': '⚠️  Timing Attack Pattern',
            'data': {
                'read_ops_per_sec': 180.0,
                'avg_read_block_size': 128,
                'session_duration': 25.0,
                'decrypt_calls': 350,
                'entropy_of_read_sequence': 0.28,
                'cache_miss_rate': 0.65,
                'reopen_frequency': 45,
                'access_time_zscore': 4.8
            }
        },
        {
            'name': '🚨 Cache Side-Channel Attack',
            'data': {
                'read_ops_per_sec': 250.0,
                'avg_read_block_size': 64,
                'session_duration': 15.0,
                'decrypt_calls': 800,
                'entropy_of_read_sequence': 0.22,
                'cache_miss_rate': 0.85,
                'reopen_frequency': 75,
                'access_time_zscore': 5.5
            }
        },
        {
            'name': '💾 Memory Dump Attempt',
            'data': {
                'read_ops_per_sec': 450.0,
                'avg_read_block_size': 32768,
                'session_duration': 8.0,
                'decrypt_calls': 2,
                'entropy_of_read_sequence': 0.92,
                'cache_miss_rate': 0.88,
                'reopen_frequency': 1,
                'access_time_zscore': 7.2
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{'─' * 80}")
        print(f"Scenario: {scenario['name']}")
        print('─' * 80)
        
        # Display key metrics
        data = scenario['data']
        print(f"  Read Ops/sec: {data['read_ops_per_sec']:.1f}")
        print(f"  Block Size: {data['avg_read_block_size']} bytes")
        print(f"  Decrypt Calls: {data['decrypt_calls']}")
        print(f"  Cache Miss Rate: {data['cache_miss_rate']:.2%}")
        print(f"  Access Time Z-Score: {data['access_time_zscore']:.2f}")
        
        # Detect
        result = detect_passive_attack(data)
        
        print(f"\n  🔍 Detection Result:")
        print(f"     Status: {result['prediction']}")
        print(f"     Attack Probability: {result['attack_probability']:.2%}")
        print(f"     Risk Level: {result['risk_level']}")
        
        if result['is_attack']:
            print(f"     ⚠️  THREAT DETECTED!")
        else:
            print(f"     ✅ SAFE")


def demo_active_attacks():
    """Demonstrate active attack detection on files"""
    from ml.detect_tamper import detect_tampering
    
    print_banner("ACTIVE ATTACK DETECTION DEMO")
    
    # Check if we have test files
    original_dir = "data/original"
    tampered_dir = "data/tampered"
    
    if not os.path.exists(original_dir) or not os.path.exists(tampered_dir):
        print("\n⚠️  Test files not found. Please run:")
        print("   python tempered_generator.py")
        return
    
    # Test original files
    print(f"\n{'─' * 80}")
    print("Testing ORIGINAL (Clean) Files")
    print('─' * 80)
    
    original_files = [f for f in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, f))][:3]
    for file in original_files:
        path = os.path.join(original_dir, file)
        result = detect_tampering(path)
        status = "✅" if "SAFE" in result else "❌"
        print(f"  {status} {file[:50]:50s} → {result}")
    
    # Test tampered files
    print(f"\n{'─' * 80}")
    print("Testing TAMPERED Files")
    print('─' * 80)
    
    tampered_files = [f for f in os.listdir(tampered_dir) if os.path.isfile(os.path.join(tampered_dir, f))][:5]
    for file in tampered_files:
        path = os.path.join(tampered_dir, file)
        result = detect_tampering(path)
        status = "❌" if "TAMPERED" in result else "✅"
        print(f"  {status} {file[:50]:50s} → {result}")


def demo_unified_detection():
    """Demonstrate unified detection system"""
    from ml.unified_attack_detector import UnifiedAttackDetector
    
    print_banner("UNIFIED DETECTION DEMO (Active + Passive)")
    
    detector = UnifiedAttackDetector()
    
    # Scenario 1: Clean file + Normal behavior
    print("\n" + "─" * 80)
    print("Scenario 1: Clean File + Normal Behavior")
    print("─" * 80)
    
    test_file = "data/original/cryptography_ml_ideas.pdf"
    if os.path.exists(test_file):
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
        detector.comprehensive_check(test_file, normal_behavior)
    else:
        print(f"⚠️  File not found: {test_file}")
    
    # Scenario 2: Tampered file + Attack behavior
    print("\n\n" + "─" * 80)
    print("Scenario 2: Tampered File + Suspicious Behavior")
    print("─" * 80)
    
    tampered_file = "data/tampered/cryptography_ml_ideas.pdf_flip"
    if os.path.exists(tampered_file):
        attack_behavior = {
            'read_ops_per_sec': 180.0,
            'avg_read_block_size': 256,
            'session_duration': 20.0,
            'decrypt_calls': 350,
            'entropy_of_read_sequence': 0.28,
            'cache_miss_rate': 0.78,
            'reopen_frequency': 45,
            'access_time_zscore': 5.2
        }
        detector.comprehensive_check(tampered_file, attack_behavior)
    else:
        print(f"⚠️  File not found: {tampered_file}")


def check_system_ready():
    """Check if system is ready for demo"""
    issues = []
    
    # Check models
    if not os.path.exists("models/tamper_model.pkl"):
        issues.append("Active attack model not trained")
    
    if not os.path.exists("models/passive_attack_model.pkl"):
        issues.append("Passive attack model not trained")
    
    # Check data
    if not os.path.exists("data/passive_attacks/passive_train.json"):
        issues.append("Passive attack dataset not generated")
    
    return issues


def main():
    print_banner("ATTACK DETECTION SYSTEM - INTERACTIVE DEMO")
    
    # Check system readiness
    issues = check_system_ready()
    
    if issues:
        print("\n⚠️  System not ready. Please complete the following:")
        for issue in issues:
            print(f"   • {issue}")
        print("\nRun: python run_complete_system.py")
        print("Then select option 8 (Run Complete Pipeline)")
        return
    
    print("\n✅ System ready!")
    
    while True:
        print("\n" + "─" * 80)
        print("DEMO MENU")
        print("─" * 80)
        print("1. Demo Passive Attack Detection")
        print("2. Demo Active Attack Detection")
        print("3. Demo Unified Detection (Both)")
        print("4. Run All Demos")
        print("0. Exit")
        print("─" * 80)
        
        choice = input("\nSelect demo (0-4): ").strip()
        
        if choice == '1':
            demo_passive_attacks()
        elif choice == '2':
            demo_active_attacks()
        elif choice == '3':
            demo_unified_detection()
        elif choice == '4':
            demo_passive_attacks()
            input("\n⏸️  Press Enter to continue to next demo...")
            demo_active_attacks()
            input("\n⏸️  Press Enter to continue to next demo...")
            demo_unified_detection()
        elif choice == '0':
            print("\n👋 Exiting demo. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 0-4.")
        
        if choice in ['1', '2', '3', '4']:
            input("\n⏸️  Press Enter to return to menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted. Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
