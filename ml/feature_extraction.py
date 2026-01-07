import os
import math
from collections import Counter

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = Counter(data)
    entropy = 0.0
    length = len(data)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def extract_features(file_path: str) -> list:
    if not os.path.exists(file_path):
        return [0] * 6  

    with open(file_path, "rb") as f:
        data = f.read()
    
    file_size = len(data)
    n = file_size
    
    if n > 0:
        byte_values = list(data)
        byte_mean = sum(byte_values) / n
        variance = sum((x - byte_mean) ** 2 for x in byte_values) / n
        byte_std = math.sqrt(variance)
        entropy = calculate_entropy(data)
    else:
        byte_mean = byte_std = entropy = 0

    header = data[:4]
    is_pdf = 1 if b"%PDF" in header else 0
    is_jpg = 1 if b"\xff\xd8\xff" in header else 0
    
    return [
        float(file_size), 
        float(entropy), 
        float(byte_mean), 
        float(byte_std), 
        float(is_pdf), 
        float(is_jpg)
    ]