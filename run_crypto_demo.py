"""
Simple Demo Script - Hybrid Encryption/Decryption with Attack Detection
Run this to see the complete system in action
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_crypto_detection import CryptoAttackDetector


def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def run_demo():
    """Run demonstration with predefined scenarios"""
    
    print_header("HYBRID ENCRYPTION/DECRYPTION WITH ATTACK DETECTION - DEMO")
    
    # Initialize detector
    print("\n🔧 Initializing system...")
    detector = CryptoAttackDetector()
    
    # Check if models are loaded
    if detector.active_model is None or detector.passive_model is None:
        print("\n❌ ERROR: Models not loaded!")
        print("\nPlease run the following commands first:")
        print("─"*80)
        print("1. Generate datasets:")
        print("   python tempered_generator.py")
        print("   python passive_data_generator.py")
        print("\n2. Train models:")
        print("   python -c \"from ml.train_model import train_model; train_model()\"")
        print("   python -c \"from ml.passive_attack_detector import train_passive_detector; train_passive_detector()\"")
        print("─"*80)
        return
    
    print("✅ System ready!")
    
    # Find test files
    original_dir = "data/original"
    if not os.path.exists(original_dir):
        print(f"\n❌ ERROR: {original_dir} not found!")
        print("Please add some files to data/original/ directory")
        return
    
    files = [f for f in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, f))]
    
    if not files:
        print(f"\n❌ ERROR: No files found in {original_dir}")
        print("Please add some files to test")
        return
    
    # Run demo scenarios
    print_header("DEMO SCENARIOS")
    
    print("\n📋 Available test files:")
    for i, file in enumerate(files[:5], 1):
        print(f"   {i}. {file}")
    
    print("\n" + "─"*80)
    print("SCENARIO 1: Normal File with Normal Behavior")
    print("─"*80)
    
    # Use first file
    test_file = os.path.join(original_dir, files[0])
    print(f"\n📄 Testing file: {files[0]}")
    
    # Run complete analysis
    results = detector.complete_analysis(test_file)
    
    # Show summary
    print("\n" + "─"*80)
    print("SUMMARY")
    print("─"*80)
    
    if results['active_attack']:
        print(f"Active Attack:  {results['active_attack']['percentage']:.2f}% probability")
    
    if results['passive_attack']:
        print(f"Passive Attack: {results['passive_attack']['percentage']:.2f}% probability")
    
    print("\n✅ Demo complete!")
    print("\nGenerated files:")
    print(f"   Encrypted: {results['encryption']['file']}")
    if results['decryption']['status'] == 'SUCCESS':
        print(f"   Decrypted: {results['decryption']['file']}")


def interactive_mode():
    """Interactive mode for testing custom files"""
    
    print_header("INTERACTIVE MODE")
    
    detector = CryptoAttackDetector()
    
    if detector.active_model is None or detector.passive_model is None:
        print("\n❌ ERROR: Models not loaded! Train them first.")
        return
    
    while True:
        print("\n" + "─"*80)
        print("OPTIONS:")
        print("─"*80)
        print("1. Test file from data/original/")
        print("2. Test custom file path")
        print("3. Test tampered file from data/tampered/")
        print("0. Exit")
        print("─"*80)
        
        choice = input("\nEnter choice (0-3): ").strip()
        
        if choice == '0':
            print("\n👋 Exiting...")
            break
        
        elif choice == '1':
            original_dir = "data/original"
            if os.path.exists(original_dir):
                files = [f for f in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, f))]
                print("\n📁 Available files:")
                for i, file in enumerate(files, 1):
                    print(f"   {i}. {file}")
                
                file_choice = input("\nEnter file number: ").strip()
                if file_choice.isdigit() and 1 <= int(file_choice) <= len(files):
                    test_file = os.path.join(original_dir, files[int(file_choice) - 1])
                    detector.complete_analysis(test_file)
                else:
                    print("❌ Invalid choice")
            else:
                print(f"❌ Directory not found: {original_dir}")
        
        elif choice == '2':
            file_path = input("\nEnter file path: ").strip()
            if os.path.exists(file_path):
                detector.complete_analysis(file_path)
            else:
                print(f"❌ File not found: {file_path}")
        
        elif choice == '3':
            tampered_dir = "data/tampered"
            if os.path.exists(tampered_dir):
                files = [f for f in os.listdir(tampered_dir) if os.path.isfile(os.path.join(tampered_dir, f))]
                print("\n📁 Available tampered files:")
                for i, file in enumerate(files[:10], 1):
                    print(f"   {i}. {file}")
                
                file_choice = input("\nEnter file number: ").strip()
                if file_choice.isdigit() and 1 <= int(file_choice) <= len(files):
                    test_file = os.path.join(tampered_dir, files[int(file_choice) - 1])
                    
                    # For tampered files, we'll encrypt them first
                    print("\n⚠️  Note: This is a tampered file. Encrypting it first...")
                    detector.complete_analysis(test_file)
                else:
                    print("❌ Invalid choice")
            else:
                print(f"❌ Directory not found: {tampered_dir}")
        
        else:
            print("❌ Invalid choice")
        
        input("\n⏸️  Press Enter to continue...")


def main():
    """Main entry point"""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--interactive' or sys.argv[1] == '-i':
            interactive_mode()
        else:
            # Test specific file
            test_file = sys.argv[1]
            if os.path.exists(test_file):
                detector = CryptoAttackDetector()
                detector.complete_analysis(test_file)
            else:
                print(f"❌ File not found: {test_file}")
    else:
        # Run demo
        run_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
