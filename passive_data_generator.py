"""
Passive Attack Dataset Generator
Simulates behavioral patterns for normal and passive attack scenarios
"""
import os
import json
import random
import numpy as np
from datetime import datetime, timedelta

PASSIVE_DATA_DIR = "data/passive_attacks"
os.makedirs(PASSIVE_DATA_DIR, exist_ok=True)

def generate_normal_behavior(num_samples=100):
    """Generate normal user behavior patterns"""
    normal_data = []
    
    for i in range(num_samples):
        # Normal behavior characteristics
        record = {
            'session_id': f'normal_{i}',
            'read_ops_per_sec': round(random.uniform(5, 20), 2),  # Normal reading speed
            'avg_read_block_size': random.randint(4096, 16384),  # Standard block sizes
            'session_duration': round(random.uniform(60, 600), 2),  # 1-10 minutes
            'decrypt_calls': random.randint(1, 10),  # Normal decrypt frequency
            'entropy_of_read_sequence': round(random.uniform(0.6, 0.85), 3),  # Moderate entropy
            'cache_miss_rate': round(random.uniform(0.05, 0.20), 3),  # Low cache miss
            'reopen_frequency': random.randint(0, 3),  # Occasional reopens
            'access_time_zscore': round(random.uniform(-1.5, 1.5), 3),  # Normal distribution
            'label': 0  # 0 = Normal
        }
        normal_data.append(record)
    
    return normal_data


def generate_passive_attack_behavior(num_samples=100):
    """Generate passive attack behavior patterns (eavesdropping, side-channel, etc.)"""
    attack_data = []
    
    attack_types = ['timing_attack', 'cache_attack', 'power_analysis', 'memory_dump']
    
    for i in range(num_samples):
        attack_type = random.choice(attack_types)
        
        if attack_type == 'timing_attack':
            # Timing attacks: repeated access with precise timing
            record = {
                'session_id': f'timing_attack_{i}',
                'read_ops_per_sec': round(random.uniform(50, 200), 2),  # Very high read rate
                'avg_read_block_size': random.randint(64, 512),  # Small blocks for timing
                'session_duration': round(random.uniform(10, 60), 2),  # Short bursts
                'decrypt_calls': random.randint(50, 500),  # Many decrypt attempts
                'entropy_of_read_sequence': round(random.uniform(0.2, 0.4), 3),  # Low entropy (repetitive)
                'cache_miss_rate': round(random.uniform(0.40, 0.70), 3),  # High cache miss
                'reopen_frequency': random.randint(10, 50),  # Frequent reopens
                'access_time_zscore': round(random.uniform(2.5, 5.0), 3),  # Anomalous timing
                'label': 1  # 1 = Passive Attack
            }
        
        elif attack_type == 'cache_attack':
            # Cache side-channel attacks
            record = {
                'session_id': f'cache_attack_{i}',
                'read_ops_per_sec': round(random.uniform(100, 300), 2),  # Very high
                'avg_read_block_size': random.randint(32, 256),  # Cache line sizes
                'session_duration': round(random.uniform(5, 30), 2),  # Quick probing
                'decrypt_calls': random.randint(100, 1000),  # Many attempts
                'entropy_of_read_sequence': round(random.uniform(0.15, 0.35), 3),  # Very low
                'cache_miss_rate': round(random.uniform(0.60, 0.90), 3),  # Very high
                'reopen_frequency': random.randint(20, 100),  # Very frequent
                'access_time_zscore': round(random.uniform(3.0, 6.0), 3),  # Highly anomalous
                'label': 1
            }
        
        elif attack_type == 'power_analysis':
            # Power analysis attacks (simulated through access patterns)
            record = {
                'session_id': f'power_analysis_{i}',
                'read_ops_per_sec': round(random.uniform(30, 80), 2),  # Moderate-high
                'avg_read_block_size': random.randint(128, 1024),  # Varied blocks
                'session_duration': round(random.uniform(120, 1800), 2),  # Long sessions
                'decrypt_calls': random.randint(200, 2000),  # Many decrypts
                'entropy_of_read_sequence': round(random.uniform(0.25, 0.45), 3),  # Low
                'cache_miss_rate': round(random.uniform(0.30, 0.60), 3),  # Moderate-high
                'reopen_frequency': random.randint(5, 20),  # Some reopens
                'access_time_zscore': round(random.uniform(2.0, 4.0), 3),  # Anomalous
                'label': 1
            }
        
        else:  # memory_dump
            # Memory dumping attempts
            record = {
                'session_id': f'memory_dump_{i}',
                'read_ops_per_sec': round(random.uniform(150, 500), 2),  # Extremely high
                'avg_read_block_size': random.randint(8192, 65536),  # Large blocks
                'session_duration': round(random.uniform(2, 20), 2),  # Very short
                'decrypt_calls': random.randint(1, 5),  # Few decrypts
                'entropy_of_read_sequence': round(random.uniform(0.85, 0.95), 3),  # High (scanning)
                'cache_miss_rate': round(random.uniform(0.70, 0.95), 3),  # Very high
                'reopen_frequency': random.randint(0, 2),  # Minimal reopens
                'access_time_zscore': round(random.uniform(4.0, 8.0), 3),  # Extremely anomalous
                'label': 1
            }
        
        attack_data.append(record)
    
    return attack_data


def save_dataset(data, filename):
    """Save dataset to JSON file"""
    filepath = os.path.join(PASSIVE_DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {len(data)} records to {filepath}")


def generate_full_dataset():
    """Generate complete passive attack dataset"""
    print("Generating passive attack detection dataset...")
    
    # Generate training data
    normal_train = generate_normal_behavior(num_samples=500)
    attack_train = generate_passive_attack_behavior(num_samples=500)
    
    # Generate test data
    normal_test = generate_normal_behavior(num_samples=100)
    attack_test = generate_passive_attack_behavior(num_samples=100)
    
    # Combine and shuffle
    train_data = normal_train + attack_train
    test_data = normal_test + attack_test
    
    random.shuffle(train_data)
    random.shuffle(test_data)
    
    # Save datasets
    save_dataset(train_data, 'passive_train.json')
    save_dataset(test_data, 'passive_test.json')
    save_dataset(normal_train, 'normal_behavior.json')
    save_dataset(attack_train, 'passive_attacks.json')
    
    print(f"\n📊 Dataset Summary:")
    print(f"   Training samples: {len(train_data)} (Normal: {len(normal_train)}, Attack: {len(attack_train)})")
    print(f"   Test samples: {len(test_data)} (Normal: {len(normal_test)}, Attack: {len(attack_test)})")
    print(f"\n✅ Passive attack dataset generation complete!")


if __name__ == "__main__":
    generate_full_dataset()
