import os
import pickle
import numpy as np
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from ml.feature_extraction import extract_features

MODEL_PATH = "models/tamper_model.pkl"

def hybrid_encrypt(file_path, public_key):
    """AES-256 Encrypts file, then RSA encrypts the AES key."""
    with open(file_path, "rb") as f:
        data = f.read()

    session_key = get_random_bytes(16) 
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(pad(data, AES.block_size))

    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    return enc_session_key, cipher_aes.iv, ciphertext

def hybrid_decrypt(enc_session_key, iv, ciphertext, private_key):
    """RSA decrypts the AES key, then AES decrypts the file."""
    try:
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)
        
        return decrypted_data
    except (ValueError, KeyError) as e:
        print(f"Cryptographic Error: {e}")
        return None

def run_pipeline(test_file):
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()

    if not os.path.exists(test_file):
        print(f"Error: File {test_file} not found.")
        return

    print(f"Processing: {test_file}")
    enc_key, iv, ciphertext = hybrid_encrypt(test_file, public_key)
    
    decrypted_content = hybrid_decrypt(enc_key, iv, ciphertext, private_key)
    
    if decrypted_content is None:
        print("Result: TAMPERED (Failed Decryption/Integrity Check)")
        return

    dec_path = "temp_decrypted_output.bin"
    with open(dec_path, "wb") as f:
        f.write(decrypted_content)

    try:
        with open(MODEL_PATH, "rb") as f:
            model_data = pickle.load(f)
            model = model_data['model']
            scaler = model_data['scaler']

        features = extract_features(dec_path)
        features_arr = np.array(features).reshape(1, -1)
        scaled_features = scaler.transform(features_arr)
        
        prediction = model.predict(scaled_features)[0]

        status = "TAMPERED" if prediction == 1 else "SAFE"
        print(f"ML Decision: {status}")

    except Exception as e:
        print(f"ML Pipeline Error: {e}")
    
    finally:
        if os.path.exists(dec_path):
            os.remove(dec_path)

if __name__ == "__main__":
    file_to_test = "data/tampered/"
    run_pipeline(file_to_test)