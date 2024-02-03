import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai  import GoogleGenerativeAIEmbeddings

import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    texts =  ""
    for pdf in pdf_docs:
        pdf_re =  PdfReader(pdf)
        for page in pdf_re.pages:
            texts+=page.extract_text()

    return texts



def get_text_chunks(text):
    text_chunk =RecursiveCharacterTextSplitter(
        chunk_size = 10000, chunk_overlap=1000
    )   
    chunk = text_chunk.split_text(text)
    return chunk


def get_vectorstore(text_chunk):
    emb = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    vs = FAISS.from_texts(text_chunk,embedding=emb)
    vs.save_local("faiss_index")
    print("Saved Vector")

def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(q):
    emb = GoogleGenerativeAIEmbeddings(model='models/embedding-001')

    newd =  FAISS.load_local("faiss_index",emb)

    docs = newd.similarity_search(q)

    chain = get_conversational_chain()
    

    res = chain(
        {"input_documents":docs,'question':q},return_only_outputs=True
    )
    print(res)
    st.write("Reply: ",res['output_text'])

def main():
    st.set_page_config("CP")
    st.header("PDF BOT")

    usinp = st.text_input("Ask Question")
    if usinp:
        user_input(usinp)

    with st.sidebar:
        st.title("Menu: ")
        pdf_docs = st.file_uploader("Upload pdf ",type=['pdf','docx'],accept_multiple_files=True)
        print(pdf_docs)
        if st.button("Submit & process"):
            with st.spinner("Processing  ...   "):
                raw_text = get_pdf_text(pdf_docs=pdf_docs)
                text_chuck =  get_text_chunks(raw_text)
                get_vectorstore(text_chuck)
                st.success("Done")

main()








