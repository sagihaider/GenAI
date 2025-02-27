import streamlit as st
import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
import time
from langchain_community.document_loaders import UnstructuredURLLoader
st.title("Ask with AI")
GOOGLE_API_KEY = "AIzaSyCodhVorPNaomfaqN4twcIJEPCU-T1MNXo"
genai.configure(api_key=GOOGLE_API_KEY)
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = genai.GenerativeModel("gemini-pro")
if "messages" not in st.session_state:
    st.session_state.messages = []
def load_documents(urls):
    loader = UnstructuredURLLoader(urls=urls)
    return loader.load()
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Ask your doubt?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("Thinking..."):
            conversation_history = "\n".join(
                [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]
            )
            for msg in st.session_state.messages:
                print(f"{msg['role']}")
                print(f"{msg['content']}")
            response = st.session_state["gemini_model"].generate_content(conversation_history)
            response_text = response.text
        # Simulate typing effect
        typed_text = ""
        for char in response_text:
            typed_text += char
            placeholder.markdown(typed_text + "▌")
            time.sleep(0.02)
        placeholder.markdown(typed_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})