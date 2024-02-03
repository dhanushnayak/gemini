import pandas as pd
import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

path = 'C://Users/Admin/Desktop/Nutanxt/Xylic_data/data/cleaned/v11.csv'

#df = pd.json_normalize(json.load(open(path)))
data = pd.read_csv(path)


def get_response(q,prompt):
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content([prompt,q])
    return res

prompt=[
    """
    You are an expert in converting English questions to return query results from pandas dataframe!.\n
    you will act as pandas data parser and try to convert question into dataframe filter or operator.\n
    Example like what is unique count of product_category that returns df['product_categpry'].nunique()\n


    """


]
    
st.set_page_config(page_title='Xylic')
st.title("Prompt")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

if submit:
    res = get_response(q=question,prompt=prompt)
    print(res)
    st.subheader("Response: ")
    st.write(res)

