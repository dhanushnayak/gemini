from dotenv import load_dotenv
load_dotenv() ## loading env variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro-vision')

def get_response(inputs,img):
    if input!='':
        res = model.generate_content([inputs,img])
    else:
        res = model.generate_content(img)
    return res.text

st.set_page_config(page_title='Gemini Image Demo')

st.header("Gemini App")
inputs = st.text_input("Input Prompt: ",key='input')

uploaded_file = st.file_uploader("Choose an image...",type=['jpg','jpeg','png'])
image=""
if uploaded_file is not None:
    image =  Image.open(uploaded_file)
    st.image(image=image,caption="Uploaded Image",use_column_width=True)

submit = st.button("Tell me about the image")

if submit:
    res =  get_response(inputs,image)
    st.write(res)
