from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
from PIL import Image

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_res(input,img,prompt):
    res = model.generate_content([input,img[0],prompt])
    return res.text

def inp_img_set(uf):
    if uf is not None:
        bd = uf.getvalue()
        image_parts = [
            {
                "mime_type": uf.type,
                "data": bd
            }
        ]
        return image_parts
    else:
        FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Gemini Image")

st.header("Gemini APP")
inp =  st.text_input("Input_Prompt: ",key='input')
uf =  st.file_uploader("Choose an image....",type=['jpg','jpeg','png'])

img = ''
if uf is not None:
    img = Image.open(uf)
    st.image(img,caption="uploaded image",use_column_width=True)

submit = st.button('Tell me about invoice')
Input_Prompt = """
your expert in understanding invoices and we will upload a image as invoice and you will have to answer any question based on invoice
image
"""

if submit:
    img_data = inp_img_set(uf)
    res = get_gemini_res(Input_Prompt,img=img_data,prompt=inp)
    st.write(res)


