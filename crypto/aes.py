from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def aes_encrypt(data):
    key = get_random_bytes(32)  # AES-256
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return key, cipher.nonce, ciphertext, tag
