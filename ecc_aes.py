'''
Example usage:
MESSAGE = b"Hello, ECC-AES!"
privKey = ECCAES.generate_ecc_private_key()
pubKey = ECCAES.generate_ecc_public_key(privKey)
encryptedMsg = ECCAES.encrypt_ECC(MESSAGE, pubKey)
decryptedMsg = ECCAES.decrypt_ECC(encryptedMsg, privKey)

print("Original Message:", MESSAGE)
print("Encrypted Message:", binascii.hexlify(encryptedMsg[0]))
print("Decrypted Message:", decryptedMsg.decode("utf-8"))
'''
from tinyec import registry
from Crypto.Cipher import AES
import hashlib
import secrets
import binascii

class ECCAES:
    @staticmethod
    def encrypt_AES_GCM(msg, secretKey):
        """
        Encrypts a message using AES-GCM mode.

        Args:
            msg (bytes): The message to be encrypted.
            secretKey (bytes): The secret key used for encryption.

        Returns:
            tuple: A tuple containing ciphertext, nonce, and authentication tag.
        """
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
        return (ciphertext, aesCipher.nonce, authTag)

    @staticmethod
    def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
        """
        Decrypts a message using AES-GCM mode.

        Args:
            ciphertext (bytes): The encrypted ciphertext.
            nonce (bytes): The nonce used during encryption.
            authTag (bytes): The authentication tag.
            secretKey (bytes): The secret key used for decryption.

        Returns:
            bytes: The decrypted plaintext message.
        """
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
        plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
        return plaintext

    @staticmethod
    def ecc_point_to_256_bit_key(point):
        """
        Converts an ECC point to a 256-bit key.

        Args:
            point (tinyec.Point): The ECC point.

        Returns:
            bytes: The 256-bit key.
        """
        sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
        sha.update(int.to_bytes(point.y, 32, 'big'))
        return sha.digest()

    @staticmethod
    def generate_ecc_private_key():
        """
        Generates a random ECC private key.

        Returns:
            int: The ECC private key.
        """
        curve = registry.get_curve('brainpoolP256r1')
        return secrets.randbelow(curve.field.n)

    @staticmethod
    def generate_ecc_public_key(privKey):
        """
        Generates the ECC public key corresponding to a given private key.

        Args:
            privKey (int): The ECC private key.

        Returns:
            tinyec.Point: The ECC public key point.
        """
        curve = registry.get_curve('brainpoolP256r1')
        return privKey * curve.g

    @staticmethod
    def generate_aes_private_key(pubKey):
        """
        Generates a random AES private key based on an ECC public key.

        Args:
            pubKey (tinyec.Point): The ECC public key.

        Returns:
            bytes: The AES private key.
        """
        curve = registry.get_curve('brainpoolP256r1')
        sharedECCKey = secrets.randbelow(curve.field.n) * pubKey
        return ECCAES.ecc_point_to_256_bit_key(sharedECCKey)

    @staticmethod
    def encrypt_ECC(msg, pubKey):
        """
        Encrypts a message using Elliptic Curve Cryptography (ECC) and AES-GCM mode.

        Args:
            msg (bytes): The message to be encrypted.
            pubKey (tinyec.Point): The ECC public key of the recipient.

        Returns:
            tuple: A tuple containing ciphertext, nonce, authentication tag, and ciphertext's public key.
        """
        curve = registry.get_curve('brainpoolP256r1')
        ciphertextPrivKey = ECCAES.generate_ecc_private_key()
        sharedECCKey = ciphertextPrivKey * pubKey
        secretKey = ECCAES.ecc_point_to_256_bit_key(sharedECCKey)
        ciphertext, nonce, authTag = ECCAES.encrypt_AES_GCM(msg, secretKey)
        ciphertextPubKey = ciphertextPrivKey * curve.g
        return (ciphertext, nonce, authTag, ciphertextPubKey)

    @staticmethod
    def decrypt_ECC(encryptedMsg, privKey):
        """
        Decrypts a message encrypted using Elliptic Curve Cryptography (ECC) and AES-GCM mode.

        Args:
            encryptedMsg (tuple): A tuple containing ciphertext, nonce, authentication tag, and ciphertext's public key.
            privKey (int): The recipient's ECC private key.

        Returns:
            bytes: The decrypted plaintext message.
        """
        curve = registry.get_curve('brainpoolP256r1')
        (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
        sharedECCKey = privKey * ciphertextPubKey
        secretKey = ECCAES.ecc_point_to_256_bit_key(sharedECCKey)
        plaintext = ECCAES.decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
        return plaintext