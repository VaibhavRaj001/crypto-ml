import numpy as np
import math
import hashlib

def entropy(data):
    probs = [data.count(byte) / len(data) for byte in set(data)]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(file_path):
    data = open(file_path, "rb").read()
    return [
        len(data),
        entropy(data),
        np.std(list(data)),
        len(set(data))
    ]
