import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Ensure authentication (Set your actual API key)
GOOGLE_API_KEY = "AIzaSyCodhVorPNaomfaqN4twcIJEPCU-T1MNXo"

# Initialize Google Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=1024,
    api_key=GOOGLE_API_KEY
)

# Define prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a chatbot"),
        ("human", "Question: {question}")
    ]
)

# Set up LangChain processing
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Streamlit UI
st.title("Try AI Model to help you for new ideas")

input_text = st.text_input("Ask your doubt here")

if input_text:
    with st.spinner("Thinking..."):
        response = chain.invoke({'question': input_text})  # Correct usage of invoke()
    st.write(response)  # Display response
