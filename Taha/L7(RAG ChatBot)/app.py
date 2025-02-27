import os
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
load_dotenv()
loader = PyPDFLoader(os.environ.get("PDF_PATH"))
data = loader.load()
print(len(data))
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(data)
print("Total number of documents:", len(docs))
from langchain_chroma import Chroma 
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3.1")
vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_type="similarity",search_kwargs={"k": 5})
retrieved_docs = retriever.invoke("Which are the most critical bugs?")
for doc in retrieved_docs:
    print(doc.page_content)