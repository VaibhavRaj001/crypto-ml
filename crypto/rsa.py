from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def rsa_encrypt(aes_key):
    public_key = RSA.import_key(open("keys/public.pem").read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(aes_key)
