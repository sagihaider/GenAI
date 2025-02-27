from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, create_react_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import re

load_dotenv()

llm = ChatOllama(model="llama3.1")
db_name=os.environ["DB_DATABASE"]
db_user = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_host = "localhost"
db_port = 3307
# chain = create_sql_query_chain(llm,db)
        
# execute_query("I want all the proposal_submission")
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",include_tables=["proposal_submission"])

toolkit = SQLDatabaseToolkit(db=db,llm=llm)
tools = toolkit.get_tools()
prompt = ChatPromptTemplate.from_messages([("system","""
    In my database, proposal_submission has a field named 'review_status', 
    which is an enum column that represents the status of the proposal:
    Value      | Description
       1       | Proposals under first review
       2       | Proposals under final review
       3       | Approved proposals
       4       | Rejected proposals
       5       | Proposals under query

    Tools available for querying:
    {tools}

    Tool names: {tool_names}

    Agent's scratchpad: {agent_scratchpad}
"""),("human","{query}")])
# agent = initialize_agent(
#     tools,
#     llm,
#     agent = "zero-shot-react-description",
#     verbose=True,
#      agent_kwargs={"prompt": prompt}
# )

query = "How many proposals are rejected"
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, handle_parsing_errors=True, verbose=True,
    max_iterations=5,  # Increase the iterations if necessary
    max_execution_time=60
)

response = agent_executor.invoke({"query": query})

print("Response :",response)