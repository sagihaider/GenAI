from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant",
    ),
    ("human", "{query}"),
])
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
st.title("LangChain Chatbot with Google Generative AI")
temperature = 0
temperature = st.number_input("Enter temprature",min_value=0.0, max_value=1.0, value="min")
query = st.text_input("Ask a question")
llm = ChatGoogleGenerativeAI(
    model=model,
    temperature=temperature,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
chain = prompt | llm | StrOutputParser()
if query:
    response = chain.invoke({"query":query})
    st.write(response)