import streamlit as st
import pycountry
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Set up Google API Key
GOOGLE_API_KEY = "AIzaSyCodhVorPNaomfaqN4twcIJEPCU-T1MNXo"

# Instantiate the LLM model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=GOOGLE_API_KEY,
)

# Get a list of all languages
languages = {lang.name: lang.alpha_2 for lang in pycountry.languages if hasattr(lang, 'alpha_2')}
language_names = sorted(languages.keys())

# Streamlit UI
st.title("AI Language Converter")

col1, col2 = st.columns(2)

with col1:
    input_language = st.selectbox("Select Input Language", language_names, index=language_names.index("English"))

with col2:
    output_language = st.selectbox("Select Output Language", language_names, index=language_names.index("German"))

input_text = st.text_area("Enter text to translate:")

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
        ("human", "{input}"),
    ]
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser  

if st.button("Translate"):
    if input_text.strip():
        with st.spinner("Translating... Please wait."):
         response = chain.invoke(
            {
                "input_language": input_language,
                "output_language": output_language,
                "input": input_text,
            }
        )
        st.subheader("Translated Text:")
        st.write(response)
    else:
        st.warning("Please enter some text to translate.")