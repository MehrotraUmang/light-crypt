'''
Todo: 
refactor saveCallback() - done
add saveCiphertet button - done
refactor acklowledgeCallback() - done
reset globalList in resetCallback
Complete Cloud tab feature
{gdrive py api, streamlit secrets for api token}

comments:
decryptCallback Rewrite, session_state objList changes, exception handling
'''
import streamlit as st
import time
from ecc_aes import *
from data_generator import *
from io import StringIO
import pandas as pd
import ast
import os


# Initialize objList in session state
if 'objList' not in st.session_state:
    st.session_state.objList = [None, None, None, None, None]

#########################################
# main process function
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

    #st.session_state.objList.append(str(privKey))
    st.session_state.objList[0] = str(privKey)

    st.session_state.eccPrivKey = st.session_state.objList[0]

    
    #st.session_state.objList.append(str(pubKey))
    st.session_state.objList[1] = str(pubKey)
    st.session_state.eccPubKey = st.session_state.objList[1]

    aesPrivKey = ecc_point_to_256_bit_key(secrets.randbelow(curve.field.n) * pubKey)

    #st.session_state.objList.append(str(aesPrivKey))
    st.session_state.objList[2] = str(aesPrivKey)
    st.session_state.aesPrivKey = st.session_state.objList[2]


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
    
    #st.session_state.objList.append(str(encryptedMsgObj))
    st.session_state.objList[3] = str(encryptedMsgObj)
    st.session_state.cipherText = st.session_state.objList[3]

    # get decrypted message using encryptedMsg and privKey
    decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
    #print("decrypted msg:", decryptedMsg)

    # get_data DECRYPTED as Decrypted text
    DECRYPTED = decryptedMsg.decode("ascii")

    #st.session_state.objList.append(str(DECRYPTED))
    st.session_state.objList[4] = str(DECRYPTED)

    print(st.session_state.objList)
    
    
#########################################
# Stereamlit button callback functions
#########################################
def saveGeneratedCallback():
    if file_type == "CSV":
        generate_csv(num_rows=st.session_state.num_row, 
                     num_columns=st.session_state.num_col, 
                     filename=st.session_state.csv_filename)
        st.info(f'{st.session_state.csv_filename} saved at project directory!')

    else:
        generate_txt(num_tokens=st.session_state.num_tokens, 
                     filename=st.session_state.txt_filename)
        st.info(f'{st.session_state.txt_filename} saved at project directory!')

def encryptCallback():
    process(st.session_state.plainText)

def decryptCallback():
    # Warning: needs exception handling if index 4 does not exist
    # st.session_state.decryptedText = st.session_state.objList[4]
    # experimental: process decrypt when clicked
    # instead of printing already decrypted value at objList[4]
    # assigned when process() is called
    try:
        # Check if there's decrypted text available
        if st.session_state.objList[4] is not None:
            st.session_state.decryptedText = st.session_state.objList[4]
        else:
            st.error("Error: No decrypted text available. Please encrypt a message first.")
    except IndexError:
        st.error("Error: Decryption failed. Please make sure you have encrypted a message first.")


def saveCiphertextCallback():
    # Warning: does not work when objList is cleared or resetCallback is called before
    # Exception handling required
    ciphertext_filename =  st.session_state.ciphertext_filename
    
    try:
        ciphertext_str = st.session_state.objList[3]  # Assuming objList[3] is a string
        
        # Convert the string representation of the dictionary to a dictionary
        try:
            ciphertext_dict = ast.literal_eval(ciphertext_str)
        except (ValueError, SyntaxError):
            st.error("Error: Unable to parse the ciphertext data.")
        try:
            if 'ciphertext' in ciphertext_dict:
                ciphertext = ciphertext_dict['ciphertext']

                # Create the "ciphertext" directory if it doesn't exist
                ciphertext_dir = 'ciphertext'
                os.makedirs(ciphertext_dir, exist_ok=True)

                # Construct the full file path
                full_file_path = os.path.join(ciphertext_dir, ciphertext_filename)

                try:
                    with open(full_file_path, 'wb') as file:
                        file.write(ciphertext)
                    st.info(f'Ciphertext saved at {full_file_path}')
                except Exception as e:
                    st.error(f"Error saving ciphertext: {str(e)}")
        
            else:
                st.error("Error: Ciphertext not found in the dictionary.")

        except UnboundLocalError:
             st.error("Error: Ciphertext not found in the dictionary.")
        
    except IndexError:
        st.error("Ciphertext not available. Please encrypt a message first.")
    
def resetCallback():
    st.session_state.plainText = ''
    st.session_state.eccPrivKey = ''
    st.session_state.eccPubKey = ''
    st.session_state.aesPrivKey = ''
    st.session_state.cipherText = ''
    st.session_state.decryptedText = ''
    st.session_state.objList = [None, None, None, None, None]
    
def acknowledgeCallback():
    alert = st.success('Acknowledge Success, Directory Cleared')
    time.sleep(3)
    alert.empty()


#########################################
# Stereamlit frontend
#########################################
st.markdown("""
                <style>
                footer {visibility: hidden;}
                </style>
                """, unsafe_allow_html=True)

st.title('Encryption & Decryption using ECC+AES')
st.subheader('LightCrypt Demonstration')
tab1, tab2, tab3, tab4 = st.tabs(["Generate Data", "Choose File", "Encrypt", "Cloud"])
with tab1:
    col1, col2, col3 = st.columns([0.2, 0.3, 0.5])
    with col1:
        file_type = st.radio("Select data type", ["CSV", "TXT"])
    if file_type == "CSV":
        with col2:    
            st.number_input(key='num_row',label='Number of rows', min_value = 1, max_value = 1000, step=1)
            st.number_input(key='num_col', label='Number of columns', min_value = 1, max_value = 1000, step=1)
        with col3:
            st.text_input('Filename', key='csv_filename',value='random_dataset.csv', max_chars=25)
    else:
        with col2:
            st.number_input(key='num_tokens', label='Number of tokens', min_value = 1, max_value = 1000, step=1)
        with col3:
            st.text_input('Filename', key='txt_filename',value='random_text.txt', max_chars=25)
    with col3: 
        st.button(label='Save', key='saveGeneratedData', 
              on_click=saveGeneratedCallback, 
            args=None,
            type="primary")
with tab2:
    uploaded_file = st.file_uploader("Upload a file", type=['txt', 'csv'])
    if uploaded_file is not None:
        # To read file as string:
        stringio = StringIO(uploaded_file.getvalue().decode("ascii"))
        string_data = stringio.read()
        st.text_input('Enter Plaintext', key="plainText", value=string_data, 
                      placeholder='Type or paste plaintext here ...')  
        if uploaded_file.type == 'text/csv':
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
        
    else:

            st.text_input('Enter Plaintext', key="plainText", 
                      placeholder='Type or paste plaintext here ...')
with tab3:
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

    txtIn_col1, empty_ol2 = st.columns([0.5, 0.5])

    with txtIn_col1:
        st.text_input('Filename', 
                      key='ciphertext_filename',
                      value='ciphertext.txt', 
                      max_chars=25)
        
        container = st.container()
        with container:
            btn_col1, btn_col2 = st.columns([0.4, 0.6])
            with btn_col1:
                st.button(label="Save", key=None,
                          help="Saves ciphertext to text file",
                          on_click=saveCiphertextCallback,
                          args=None,
                          type='primary',
                          use_container_width=False)

            with btn_col2:
                st.button(label='Reset', key=None, 
                          help='Click to reset all values', 
                          on_click=resetCallback, 
                          args=None,
                          type="secondary", 
                          use_container_width=False)



with tab4:
    st.button(label='Upload', key=None, 
              help='Acknowledge will delete input file contents', 
              on_click=acknowledgeCallback, 
              args=None,
              type="primary", 
              use_container_width=False)
    
    st.button(label='Acknowledge', key=None, 
              help='Acknowledge will delete input file contents', 
              on_click=acknowledgeCallback, 
              args=None,
              type="secondary", 
              use_container_width=False)

    