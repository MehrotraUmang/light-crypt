import eel
from ecc_aes import *

eel.init('web')
@eel.expose
def process(task):
    MESSAGE = task
    msg = bytes(MESSAGE, encoding="ascii")
    #print("original msg: ", msg)

    # get_data privKey as ECC Private Key
    privKey = secrets.randbelow(curve.field.n)
    # print("privKey: ", privKey)

    # get_data pubKey as ECC Public Key
    pubKey = privKey * curve.g
    # print("pubKey: ", pubKey)

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

    # get decrypted message using encryptedMsg and privKey
    decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
    #print("decrypted msg:", decryptedMsg)

    # get_data DECRYPTED as Decrypted text
    DECRYPTED = decryptedMsg.decode("ascii")

    list.append(str(DECRYPTED))
    print(list)

    return list

eel.start('index.html', mode='chrome')