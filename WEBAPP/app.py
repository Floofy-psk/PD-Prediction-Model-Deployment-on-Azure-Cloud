import requests
import SessionState
import streamlit as st
import os
from Crypto.Cipher import AES
import sys
import abc
from py3compat import *

KEYSIZE=16 
BLOCKSIZE=16

key=os.urandom(KEYSIZE)
iv=os.urandom(BLOCKSIZE)
key=b'\xa3\x83W\x85\xa3r\n\x97x)F\x8f\x08s&\xb7'
iv= b']\xdd7\xd9\xa1f*\xd3!\x89\x9e\x04\xfb\x99\x0e\xb8'

def pad(data_to_pad, block_size):
    padding_len = block_size-len(data_to_pad)%block_size    
    padding = bchr(padding_len)*padding_len
    return data_to_pad + padding

def unpad(padded_data, block_size, style='pkcs7'):
    pdata_len = len(padded_data)
    if pdata_len == 0:
        raise ValueError("Zero-length input cannot be unpadded")
    if pdata_len % block_size:
        raise ValueError("Input data is not padded")
    if style in ('pkcs7', 'x923'):
        padding_len = bord(padded_data[-1])
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if style == 'pkcs7':
            if padded_data[-padding_len:]!=bchr(padding_len)*padding_len:
                raise ValueError("PKCS#7 padding is incorrect.")
        else:
            if padded_data[-padding_len:-1]!=bchr(0)*(padding_len-1):
                raise ValueError("ANSI X.923 padding is incorrect.")
    elif style == 'iso7816':
        padding_len = pdata_len - padded_data.rfind(bchr(128))
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padding_len>1 and padded_data[1-padding_len:]!=bchr(0)*(padding_len-1):
            raise ValueError("ISO 7816-4 padding is incorrect.")
    else:
        raise ValueError("Unknown padding style")
    return padded_data[:-padding_len]


pd_classes = ['Control',
 'PD',]
tumor_classes = ['Not Tumor',
 'Tumor',]

classes_and_models = {
    "parkinson": {
        "classes": pd_classes,
        "model_name": "parkinson_disease_model" 
    },
    "brain_tumor": {
        "classes": tumor_classes,
        "model_name": "brain_tumor_disease_model"
    }
}

### Streamlit code (works as a straigtht-forward script) ###
st.title("Welcome to Disease Prediction using MRI")
st.header("Identify whether a person has the selected disease or not!")
@st.cache # cache the function so predictions aren't always redone (Streamlit refreshes every click)
def make_prediction(image, model, class_names):
    """
    Takes an image and uses model (a trained TensorFlow model) to make a
    prediction.
    Returns:
     pred_class (prediction class from class_names)
    """
    cipher=AES.new(key,AES.MODE_CBC,iv)
    image=cipher.encrypt(pad(image,BLOCKSIZE))
    if(model=="parkinson_disease_model"):
        url = "https://mri-endpoint.azurewebsites.net"
    elif(model=="brain_tumor_disease_model"):
        url= ""
        
    payload = {}
    files=[
    ('imagefile',('input_img',image,'image/jpeg'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return response.text

# Pick the model version
choose_model = st.sidebar.selectbox(
    "Select the Disease you want to predict:",
    ("Parkinson's Disease", 
     "Brain Tumor") 
)

# Model choice logic
if choose_model == "Parkinson's Disease":
    CLASSES = classes_and_models["parkinson"]["classes"]
    MODEL = classes_and_models["parkinson"]["model_name"]
else:
    CLASSES = classes_and_models["brain_tumor"]["classes"]
    MODEL = classes_and_models["brain_tumor"]["model_name"]

# Display info about model and classes
if st.checkbox("Show classes"):
    st.write(f"You chose {MODEL}, these are the classes it can identify the disease into:\n", CLASSES)

# File uploader allows user to add their own image
uploaded_file = st.file_uploader(label="Upload a MRI image",
                                 type=["png", "jpeg", "jpg"])

# Setup session state to remember state of app so refresh isn't always needed
# See: https://discuss.streamlit.io/t/the-button-inside-a-button-seems-to-reset-the-whole-app-why/1051/11 
session_state = SessionState.get(pred_button=False)

# Create logic for app flow
if not uploaded_file:
    st.warning("Please upload an image.")
    st.stop()
else:
    session_state.uploaded_image = uploaded_file.read()
    st.image(session_state.uploaded_image, use_column_width=True)
    pred_button = st.button("Predict")

# Did the user press the predict button?
if pred_button:
    session_state.pred_button = True 

if session_state.pred_button:
    session_state.pred_class = make_prediction(session_state.uploaded_image, model=MODEL, class_names=CLASSES)
    st.write(f"Prediction: {session_state.pred_class}")

    # # Create feedback mechanism (building a data flywheel)
    # session_state.feedback = st.selectbox(
    #     "Is this correct?",
    #     ("Select an option", "Yes", "No"))
    # if session_state.feedback == "Select an option":
    #     pass
    # elif session_state.feedback == "Yes":
    #     st.write("Thank you for your feedback!")
    #     # Log prediction information to terminal (this could be stored in Big Query or something...)
    #     print(update_logger(image=session_state.image,
    #                         model_used=MODEL,
    #                         pred_class=session_state.pred_class,
    #                         pred_conf=session_state.pred_conf,
    #                         correct=True))
    # elif session_state.feedback == "No":
    #     session_state.correct_class = st.text_input("What should the correct label be?")
    #     if session_state.correct_class:
    #         st.write("Thank you for that, we'll use your help to make our model better!")
    #         # Log prediction information to terminal (this could be stored in Big Query or something...)
    #         print(update_logger(image=session_state.image,
    #                             model_used=MODEL,
    #                             pred_class=session_state.pred_class,
    #                             pred_conf=session_state.pred_conf,
    #                             correct=False,
    #                             user_label=session_state.correct_class))

# TODO: code could be cleaned up to work with a main() function...
# if __name__ == "__main__":
#     main()