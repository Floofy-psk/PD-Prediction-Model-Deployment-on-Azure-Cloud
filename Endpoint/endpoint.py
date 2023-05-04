from flask import Flask, render_template ,request,jsonify
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import cv2
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


app =Flask(__name__)
path = os.getcwd()
model_path = os.path.join(path, 'Trained_Model')
img_width, img_height = 224, 224
# load pre-trained model
model_name = 'my_model.h5'
model_path_new = os.path.join(model_path, model_name)
loaded_model = tf.keras.models.load_model(model_path_new)

@app.route('/',methods=['POST'])
def predict():
    imagefile=request.files['imagefile']
    cipher2=AES.new(key,AES.MODE_CBC,iv)
    imagefile=unpad(cipher2.decrypt(imagefile),BLOCKSIZE)
    img = cv2.imdecode(np.fromstring(imagefile.read(), np.uint8),cv2.IMREAD_UNCHANGED)
    # image_path = "./images/"+ imagefile.filename
    # imagefile.save(image_path)
    class_list = ["control","pd"] #cd=0,pd=1
    # img =cv2.imread(imagefile)
    img=tf.image.resize(img,(img_width, img_height))
    img=img/255
    print(f'Size of image: {img.shape}')
    img = np.expand_dims(img, axis=0)
    print(f'Changed size of image: {img.shape}')
    predictions = loaded_model.predict(img)
    label_index = np.argmax(predictions)
    print(label_index)
    label_class_name = class_list[label_index]
    print(label_class_name)
    return jsonify(label_class_name)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))