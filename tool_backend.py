from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode,tools_condition
from dotenv import load_dotenv
import sqlite3
import requests

load_dotenv()  # Load environment variables from .env file
#-------------------------------------------------
# 1. LLM Setup
#-------------------------------------------------

llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0.6)

#-------------------------------------------------
# 2. Tool Setup
#-------------------------------------------------
# Tools
search_tool = DuckDuckGoSearchRun(region='us-en')

@tool
def calculator_tool(first_num:float, sec_num:float, operation:str,) -> dict:
    """
    Performs a basic arithmetic operation (addition, subtraction, multiplication, or division) on two numbers.
    """
    try:
        if operation == "add":
            result=first_num + sec_num
        elif operation == "subtract":
            result=first_num - sec_num
        elif operation == "multiply":
            result=first_num * sec_num
        elif operation == "divide":
            if sec_num != 0:
                result=first_num / sec_num
            else:
                return "Error: Division by zero is not allowed."
        else:
            return "Error: Invalid operation. Please use 'add', 'subtract', 'multiply', or 'divide'."

        return {'first_num': first_num, 'sec_num': sec_num, 'operation': operation, 'result': result}
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_stock_price(symbol: str) -> dict:
    """"
    Fetch latest stock price for a given symbol (eg.AAPL,MSFT)
    from Alpha Vantage using the API given in the url
    
    """
    url="" 
    res=requests.get(url)
    return res.json()

tools=[search_tool,calculator_tool,get_stock_price]

llm_with_tool = llm.bind_tools(tools)

#-------------------------------------------------
# 3. State Setup
#-------------------------------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#-------------------------------------------------
# 4. Node Setup
#-------------------------------------------------
def chat_node(state: ChatState):
    "LLM node that answers the user query by ownself or using the given tools"
    messages = state['messages']
    response = llm_with_tool.invoke(messages)
    return {'messages':response}

t_node = ToolNode(tools)

#-------------------------------------------------
# 5. Checkpointer Setup
#-------------------------------------------------
conn = sqlite3.connect(database='langgraph_chatbot.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

#-------------------------------------------------
# 6. Graph Setup
#-------------------------------------------------
graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_node('tools',t_node)

graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)

graph.add_edge('tools','chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

#-------------------------------------------------
# 7. Helper Functions
#-------------------------------------------------
def retrieve_all_thread_ids():
    all_thread = set()
    for checkpoint in checkpointer.list(None):
        all_thread.add(checkpoint.config['configurable']['thread_id'])
    return list(all_thread)