import os
import streamlit as st
from dotenv import load_dotenv
import  google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def input_image_setup(uf):
    if uf is not None:
        bytes_data = uf.getvalue()
        image_parts = [
            {
                "mime_type": uf.type,
                "data": bytes_data
             }
        ]
        return image_parts
    else:
        return FileNotFoundError("No file uploaded")
    
def get_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-pro-vision")
    res = model.generate_content([input_prompt,image[0]])
    return res.text

st.set_page_config(page_title="Health App")

st.header("Health Set App")
uf = st.file_uploader("Choose an image....", type=['jpg','jpeg','png'])
img  = ""

if uf is not None:
    img = Image.open(uf)
    st.image(img,caption='Uploaded image...')

sub = st.button("Tell me about the total calories")



inp_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food items with calories intake in below format

1. Item 1 - no of calories
2. Item 2 - no of calories
-----
-----
-----

finally you can also mention whether the food is healthy or not and also mention 
the percentage split of the ratio of carbohydrates,fats, sugar and protein things required in our diet
"""


if sub:
    inp=input_image_setup(uf)
    res = get_response(input_prompt=inp_prompt,image=inp)
    st.write(res)
