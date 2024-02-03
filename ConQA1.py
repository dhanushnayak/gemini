from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_response(quest):
    res = chat.send_message(quest,stream=True)
    return res

st.set_page_config(page_title='Q&A Demo')

st.header("LLM Q&A")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("input: ",key='input')
submit = st.button("Ask the Question")

if submit and input:
    res = get_response(input)

    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is ")
    for chuck in res:
        st.write(chuck.text)
        st.session_state['chat_history'].append(("Bot",chuck.text))

st.subheader("The Chat history is")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
