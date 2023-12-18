import os
from dotenv import load_dotenv
import openai
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from funciones import utils
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#--------- WEB -------------------------------------------

st.header("Simple Analizador de PDF")


#--------- SUBIR PDF Y VECTORIZARLO -----------------------

st.subheader("1. Cargar PDF")

pdf = st.file_uploader("Sube tu PDF", type='pdf')



if pdf is not None:
    pdf_reader = PdfReader(pdf)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
    chunks = text_splitter.split_text(text=text)

    embeddings = OpenAIEmbeddings()

    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)

    #Get file name
    file_name = utils.get_filename_without_extension(pdf.name)

#--------- HACER CONSULTA -----------------------

st.subheader("2. Hacer consultas")

user_input = st.text_input("La pregunta")

if user_input:
    
    #Texto similares para contexto
    docs = VectorStore.similarity_search(query=user_input, k=3)

    #Entender la pregunta:
    llm = OpenAI(model_name='gpt-3.5-turbo')
    chain = load_qa_chain(llm=llm, chain_type="stuff")

    #Crear respuesta
    response = chain.run(input_documents=docs, question=user_input)

    st.write(response)



