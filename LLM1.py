from dotenv import load_dotenv
load_dotenv() ## loading env variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
def get_response(qest):
    global model
    res = model.generate_content(qest)
    return res.text



## print(get_response("What is Life?"))  ############## Testing response  #################


#### Streamlit App ####

st.set_page_config(page_title="Q&A Demo")

st.header("LLM APP")

inputs =  st.text_input("Input: ",key='input')
submit = st.button("Ask Question")

if submit:
    res =  get_response(inputs)
    st.write(res)

    
