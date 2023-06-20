"""
Todo: eel variables for the followning:
    ECC Private Key : privKey
    AES Key         : secretKey
    ECC Public Key  : pubKey
    message         : MESSAGE 
    ciphertext      : encryptedMsgObj
    decrypted text  : DECRYPTED
"""

from tinyec import registry
from Crypto.Cipher import AES
import hashlib
import secrets
import binascii
import eel
import logic.todo_controller

eel.init('web')

secretKey = None


def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)


def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext


def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()


curve = registry.get_curve('brainpoolP256r1')


def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)


def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext


@eel.expose
def process(task):
    MESSAGE = task
    msg = bytes(MESSAGE, encoding="ascii")
    #print("original msg: ", msg)

    # get_data privKey as ECC Private Key
    privKey = secrets.randbelow(curve.field.n)
    #print("privKey: ", privKey)

    # get_data pubKey as ECC Public Key
    pubKey = privKey * curve.g
    #print("pubKey: ", pubKey)

    list = []
    list.append(str(privKey))
    list.append(str(pubKey))
    list.append(str(ecc_point_to_256_bit_key(
        secrets.randbelow(curve.field.n) * pubKey)))

    print("\n\naes key: ", ecc_point_to_256_bit_key(
        secrets.randbelow(curve.field.n) * pubKey))

    encryptedMsg = encrypt_ECC(msg, pubKey)
    encryptedMsgObj = {
        'ciphertext': binascii.hexlify(encryptedMsg[0]),
        'nonce': binascii.hexlify(encryptedMsg[1]),
        'authTag': binascii.hexlify(encryptedMsg[2]),
        'ciphertextPubKey': hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:]
    }
    print("encrypted msg:", encryptedMsgObj)
    # get_data encryptedMsgObj as ciphertext
    list.append(str(encryptedMsgObj))

    decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
    #print("decrypted msg:", decryptedMsg)

    # get_data DECRYPTED as Decrypted text
    DECRYPTED = decryptedMsg.decode("ascii")
    list.append(str(DECRYPTED))
    print(list)

    return list


eel.start('index.html')