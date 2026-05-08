"""
Complete Cryptography + ML Attack Detection System
Runs the entire pipeline: data generation, training, and detection
"""
import os
import sys

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def main():
    print_header("CRYPTOGRAPHY + ML ATTACK DETECTION SYSTEM")
    print("This system detects both ACTIVE and PASSIVE attacks:")
    print("  • ACTIVE ATTACKS: File tampering, data modification")
    print("  • PASSIVE ATTACKS: Eavesdropping, timing attacks, cache attacks")
    print("\n" + "=" * 80)
    
    while True:
        print("\n📋 MAIN MENU")
        print("-" * 80)
        print("1. Generate Active Attack Dataset (tampered files)")
        print("2. Generate Passive Attack Dataset (behavioral data)")
        print("3. Train Active Attack Detector")
        print("4. Train Passive Attack Detector")
        print("5. Test Active Attack Detection")
        print("6. Test Passive Attack Detection")
        print("7. Run Unified Detection (Both Active + Passive)")
        print("8. Run Complete Pipeline (Generate + Train + Test)")
        print("9. View System Status")
        print("0. Exit")
        print("-" * 80)
        
        choice = input("\nEnter your choice (0-9): ").strip()
        
        if choice == '1':
            print_header("GENERATING ACTIVE ATTACK DATASET")
            import tempered_generator
            tempered_generator.generate_tampered()
        
        elif choice == '2':
            print_header("GENERATING PASSIVE ATTACK DATASET")
            import passive_data_generator
            passive_data_generator.generate_full_dataset()
        
        elif choice == '3':
            print_header("TRAINING ACTIVE ATTACK DETECTOR")
            from ml.train_model import train_model
            train_model()
        
        elif choice == '4':
            print_header("TRAINING PASSIVE ATTACK DETECTOR")
            from ml.passive_attack_detector import train_passive_detector
            train_passive_detector()
        
        elif choice == '5':
            print_header("TESTING ACTIVE ATTACK DETECTION")
            test_active_detection()
        
        elif choice == '6':
            print_header("TESTING PASSIVE ATTACK DETECTION")
            from ml.passive_attack_detector import test_passive_detector
            test_passive_detector()
        
        elif choice == '7':
            print_header("UNIFIED ATTACK DETECTION")
            from ml.unified_attack_detector import main as unified_main
            unified_main()
        
        elif choice == '8':
            print_header("RUNNING COMPLETE PIPELINE")
            run_complete_pipeline()
        
        elif choice == '9':
            print_header("SYSTEM STATUS")
            show_system_status()
        
        elif choice == '0':
            print("\n👋 Exiting system. Goodbye!")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice. Please enter a number between 0-9.")
        
        input("\n⏸️  Press Enter to continue...")


def test_active_detection():
    """Test active attack detection on sample files"""
    from ml.detect_tamper import detect_tampering
    
    print("Testing active attack detection on sample files...\n")
    
    # Test original files
    original_dir = "data/original"
    if os.path.exists(original_dir):
        print("📁 Testing ORIGINAL files:")
        print("-" * 80)
        files = [f for f in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, f))][:3]
        for file in files:
            path = os.path.join(original_dir, file)
            result = detect_tampering(path)
            print(f"  {file[:50]:50s} → {result}")
    
    # Test tampered files
    tampered_dir = "data/tampered"
    if os.path.exists(tampered_dir):
        print("\n📁 Testing TAMPERED files:")
        print("-" * 80)
        files = [f for f in os.listdir(tampered_dir) if os.path.isfile(os.path.join(tampered_dir, f))][:5]
        for file in files:
            path = os.path.join(tampered_dir, file)
            result = detect_tampering(path)
            print(f"  {file[:50]:50s} → {result}")


def run_complete_pipeline():
    """Run the complete pipeline from data generation to testing"""
    print("Running complete pipeline...\n")
    
    # Step 1: Generate active attack data
    print("STEP 1/6: Generating active attack dataset...")
    import tempered_generator
    tempered_generator.generate_tampered()
    
    # Step 2: Generate passive attack data
    print("\nSTEP 2/6: Generating passive attack dataset...")
    import passive_data_generator
    passive_data_generator.generate_full_dataset()
    
    # Step 3: Train active detector
    print("\nSTEP 3/6: Training active attack detector...")
    from ml.train_model import train_model
    train_model()
    
    # Step 4: Train passive detector
    print("\nSTEP 4/6: Training passive attack detector...")
    from ml.passive_attack_detector import train_passive_detector
    train_passive_detector()
    
    # Step 5: Test active detector
    print("\nSTEP 5/6: Testing active attack detector...")
    test_active_detection()
    
    # Step 6: Test passive detector
    print("\nSTEP 6/6: Testing passive attack detector...")
    from ml.passive_attack_detector import test_passive_detector
    test_passive_detector()
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
    print("=" * 80)
    print("\nYou can now use option 7 to run unified detection on new data.")


def show_system_status():
    """Show current system status"""
    print("Checking system components...\n")
    
    # Check datasets
    print("📊 DATASETS:")
    print("-" * 80)
    
    original_dir = "data/original"
    if os.path.exists(original_dir):
        count = len([f for f in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, f))])
        print(f"  ✅ Original files: {count} files")
    else:
        print(f"  ❌ Original files: Not found")
    
    tampered_dir = "data/tampered"
    if os.path.exists(tampered_dir):
        count = len([f for f in os.listdir(tampered_dir) if os.path.isfile(os.path.join(tampered_dir, f))])
        print(f"  ✅ Tampered files: {count} files")
    else:
        print(f"  ❌ Tampered files: Not found")
    
    passive_dir = "data/passive_attacks"
    if os.path.exists(passive_dir):
        files = os.listdir(passive_dir)
        print(f"  ✅ Passive attack data: {len(files)} files")
    else:
        print(f"  ❌ Passive attack data: Not found")
    
    # Check models
    print("\n🤖 MODELS:")
    print("-" * 80)
    
    active_model = "models/tamper_model.pkl"
    if os.path.exists(active_model):
        size = os.path.getsize(active_model) / 1024
        print(f"  ✅ Active attack model: {size:.2f} KB")
    else:
        print(f"  ❌ Active attack model: Not trained")
    
    passive_model = "models/passive_attack_model.pkl"
    if os.path.exists(passive_model):
        size = os.path.getsize(passive_model) / 1024
        print(f"  ✅ Passive attack model: {size:.2f} KB")
    else:
        print(f"  ❌ Passive attack model: Not trained")
    
    # Check logs
    print("\n📝 LOGS:")
    print("-" * 80)
    
    log_dir = "logs"
    if os.path.exists(log_dir):
        logs = os.listdir(log_dir)
        print(f"  ✅ Detection logs: {len(logs)} files")
    else:
        print(f"  ℹ️  No logs yet")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
