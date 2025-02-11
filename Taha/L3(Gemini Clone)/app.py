from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = "gemini-1.5-pro"
models = {
    "gemini-2.0-flash": "Gemini 2.0 Flash - Next-gen multimodal generation",
    "gemini-2.0-flash-lite-preview-02-05": "Gemini 2.0 Flash-Lite - Optimized for cost efficiency",
    "gemini-1.5-flash": "Gemini 1.5 Flash - Fast and versatile performance",
    "gemini-1.5-flash-8b": "Gemini 1.5 Flash-8B - High volume, lower intelligence tasks",
    "gemini-1.5-pro": "Gemini 1.5 Pro - Complex reasoning tasks",
    "gemini-1.0-pro": "Gemini 1.0 Pro (Deprecated 2/15/2025) - Natural language tasks",
    "text-embedding-004": "Text Embedding - Measuring relatedness of text strings",
    "aqa": "AQA - Providing source-grounded answers",
}

model = st.selectbox("Choose a model:", list(models.keys()), format_func=lambda x: models[x])
st.session_state.model = model
st.title("Gemini Clone")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        llm = ChatGoogleGenerativeAI(
        model=st.session_state.model,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        )
        response = llm.invoke(prompt)  # Use invoke() to generate response
        st.markdown(response.content)  
    st.session_state.messages.append({"role": "assistant", "content": response})