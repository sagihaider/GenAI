import os
from langchain.chains import create_sql_query_chain
from mysql.connector import ProgrammingError
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import re
from dotenv import load_dotenv
load_dotenv()
llm = ChatOllama(model="mistral")
result = llm.invoke("Tell me a joke")
print(result)
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
db_name=os.environ["DB_DATABASE"]
print(db_name)
db_user = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_host = "localhost"
db_port = 3307
# chain = create_sql_query_chain(llm,db)
def extract_sql_query(text):
    # Define a regex pattern to capture SQL queries
    sql_pattern = re.compile(r"(SELECT\s[\s\S]+?;)", re.IGNORECASE)
    
    # Search for the pattern in the text
    match = sql_pattern.findall(text)
    return [query.strip() for query in match][0]
def execute_query(question):
    try:
        response = chain.invoke({"question": question})
        response = re.sub(r'<think>.*?</think>', '', response,flags=re.DOTALL).strip()
        query = extract_sql_query(response)
        print(query)
        result = db.run(query)
        print(result)
    except ProgrammingError as e:
        print(f"An error occurred: {e}")
        
# execute_query("I want all the proposal_submission")
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",include_tables=["users","proposal_submission"])
def get_schema(_):
    return db.get_table_info()

template = """
Based on the table schema below, generate a SQL query that answers the question.
Do not include explanations, only return the raw SQL query.
If someone specifically asks for a specific status of proposal_submission then the field where to find status is review_status,
Under First Review review_status is '1'
Under Final Review review_status is '2'
Accepted review_status is '3'
Rejected review_status is '4'
Under Query review_status is '5'
{schema}

Question: {question}
SQL Query:
"""


prompt = ChatPromptTemplate.from_template(template)
sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm.bind(stop=["\n"])
    | StrOutputParser()
)

template ="""
Based on the table schema below, question, sql query and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}
"""

prompt = ChatPromptTemplate.from_template(template)

def run_query(query):
    print("Query:", query)
    return db.run(query)
nlg_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(schema=get_schema,response = lambda vars: run_query(vars["query"]))
    # RunnablePassthrough.assign(query=sql_chain).assign(schema=get_schema,response = lambda vars: print("Print",vars))
    | prompt
    | llm
    | StrOutputParser()
)
result = nlg_chain.invoke({"question": "how many rejected proposal_submission are there"})
print(result)