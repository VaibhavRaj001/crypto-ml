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
    with open(file_path, "rb") as f:
        data = f.read()

    file_size = os.path.getsize(file_path)
    entropy = calculate_entropy(data)

    byte_values = list(data)
    byte_mean = sum(byte_values) / len(byte_values) if byte_values else 0
    byte_std = (
        sum((b - byte_mean) ** 2 for b in byte_values) / len(byte_values)
    ) ** 0.5 if byte_values else 0

    return [
        file_size,
        entropy,
        byte_mean,
        byte_std
    ]
