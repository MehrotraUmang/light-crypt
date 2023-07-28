'''
Todo: 
- solve globalList access error
- rewrite decryptFunction
'''
import streamlit as st
from ecc_aes import *
from io import StringIO


globalList = []

#########################################
# main process funciton
#########################################
def process(message):
    MESSAGE = message
    msg = bytes(MESSAGE, encoding="ascii")
    #print("original msg: ", msg)

    # get_data privKey as ECC Private Key
    privKey = secrets.randbelow(curve.field.n)
    # print("privKey: ", privKey)

    # get_data pubKey as ECC Public Key
    pubKey = privKey * curve.g
    # print("pubKey: ", pubKey)

    objList = []

    objList.append(str(privKey))
    st.session_state.eccPrivKey = objList[0]

    objList.append(str(pubKey))
    st.session_state.eccPubKey = objList[1]

    objList.append(str(ecc_point_to_256_bit_key(
        secrets.randbelow(curve.field.n) * pubKey)))
    st.session_state.aesPrivKey = objList[2]


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
    objList.append(str(encryptedMsgObj))
    st.session_state.cipherText = objList[3]

    # get decrypted message using encryptedMsg and privKey
    decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
    #print("decrypted msg:", decryptedMsg)

    # get_data DECRYPTED as Decrypted text
    DECRYPTED = decryptedMsg.decode("ascii")

    objList.append(str(DECRYPTED))
    print(objList)

    return objList
    
#########################################
# Stereamlit button callback functions
#########################################
def encryptCallback():
    process(st.session_state.plainText)

def decryptCallback():
    st.session_state.decryptedText = st.session_state.plainText
    
def resetCallback():
    st.session_state.plainText = ''
    st.session_state.eccPrivKey = ''
    st.session_state.eccPubKey = ''
    st.session_state.aesPrivKey = ''
    st.session_state.cipherText = ''
    st.session_state.decryptedText = ''
    

#########################################
# Stereamlit frontend
#########################################
st.title('Encryption & Decryption using ECC+AES')
st.subheader('LightCrypt Demonstration')

uploaded_file = st.file_uploader("Upload a file", type=['txt'])
if uploaded_file is not None:
    # To read file as string:
    stringio = StringIO(uploaded_file.getvalue().decode("ascii"))
    string_data = stringio.read()
    st.text_input('Enter Plaintext', key="plainText", value=string_data, 
                  placeholder='Type or paste plaintext here ...')  
else:
    
        st.text_input('Enter Plaintext', key="plainText", 
                  placeholder='Type or paste plaintext here ...')

heightFix = None
st.button(label='Encrypt', key='encryptBtn', 
          on_click=encryptCallback,
        help='Click to generate keys and encrypt text', 
        args=None,
        type="primary", 
        use_container_width=False)
st.text_area(label='ECC Private Key', value="", 
             key='eccPrivKey', 
             help='Randomly generated ECC Private Key', 
             on_change=None,
             height=heightFix)
st.text_area(label='ECC Public Key', value="", 
             key='eccPubKey', 
             help='Randomly generated ECC Public Key', 
             on_change=None,
             height=heightFix)
st.text_area(label='AES Private Key', value="", 
             key='aesPrivKey', 
             help='Randomly generated AES Private Key', 
             on_change=None,
             height=heightFix)
st.text_area(label='Encrypted Message Payload', value="", 
             key='cipherText', 
             help='Encrypted message payload contains ciphertext and keys', 
             on_change=None,
             height=heightFix)
st.button(label='Decrypt', key='decryptBtn', 
          help='Click to decrypt ciphertext object', 
          on_click=decryptCallback, 
          args=None,
          type="primary", 
          use_container_width=False)
st.text_area(label='Decrypted Plaintext', value="", 
             key='decryptedText', 
             help='Decrypted Text',
             height=heightFix)
st.button(label='Reset', key=None, 
          help='Click to reset all values', 
          on_click=resetCallback, 
          args=None,
          type="secondary", 
          use_container_width=False)
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


