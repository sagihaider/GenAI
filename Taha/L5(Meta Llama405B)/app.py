from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

template = """Question: {question}

Answer: Let's think step-by-step`
"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1")

chain = prompt | model

print(chain.invoke({"question": "Who is the author of the book 'To Kill a Mockingbird'?"}))