'''
Example usage:
MESSAGE = b"Hello, ECC-AES!"
privKey = secrets.randbelow(curve.field.n)
pubKey = privKey * curve.g
encryptedMsg = encrypt_ECC(MESSAGE, pubKey)
decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
print("Original Message:", MESSAGE)
print("Encrypted Message:", binascii.hexlify(encryptedMsg[0]))
print("Decrypted Message:", decryptedMsg.decode("utf-8"))
'''

from tinyec import registry
from Crypto.Cipher import AES
import hashlib
import secrets
import binascii


secretKey = None

# Encrypts a message using AES-GCM mode
def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

# Decrypts a message using AES-GCM mode
def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

# Converts an ECC point to a 256-bit key
def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

# Initialize the curve for ECC operations
curve = registry.get_curve('brainpoolP256r1')

# Elliptic Curve Cryptography (ECC) encryption
def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)

# Elliptic Curve Cryptography (ECC) decryption
def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext

def generate_ecc_private_key():
    return secrets.randbelow(curve.field.n)

def generate_ecc_public_key(privKey):
    return privKey * curve.g

def generate_aes_private_key(pubKey):
    return ecc_point_to_256_bit_key(secrets.randbelow(curve.field.n) * pubKey)