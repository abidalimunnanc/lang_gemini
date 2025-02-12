from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from github import fetch_github_issues
from note import note_tool
from langchain.tools import Tool

load_dotenv()


def connect_to_vstore():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="agent_db",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore


vstore = connect_to_vstore()
add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in [
    "yes",
    "y",
]

if add_to_vectorstore:
    owner = "techwithtim"
    repo = "Flask-Web-App-Tutorial"
    issues = fetch_github_issues(owner, repo)

    try:
        vstore.delete_collection()
    except:
        pass

    vstore = connect_to_vstore()
    vstore.add_documents(issues)

    # results = vstore.similarity_search("flash messages", k=3)
    # for res in results:
    #     print(f"* {res.page_content} {res.metadata}")

retriever = vstore.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    "github_search",
    "Search for information about github issues. For any questions about github issues, you must use this tool!",
)

# prompt = hub.pull("hwchase17/openai-functions-agent")
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = """
You are an AI personal assistant with context awareness. 
You can retrieve information, take notes, and assist with GitHub issues.
Use external tools when needed and always provide concise, helpful responses.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content="{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)



llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

note_tools = Tool(
    name="note_tool",
    func=note_tool,
    description="Stores user notes. Provide a note as a string.",
)

tools = [retriever_tool]

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    result = agent_executor.invoke(
    {
        "chat_history": [
            HumanMessage(content="hi! my name is bob"),
            AIMessage(content="Hello Bob! How can I assist you today?"),
        ],
        "input": question,
    }
)
    print(result["output"])