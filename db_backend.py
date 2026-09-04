import os
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="openai/gpt-oss-120b",api_key = api_key)

class ChatbotState(TypedDict):

    messages: Annotated[list['BaseMessage'], add_messages]


def chat_node(state: ChatbotState):

    messages = state['messages']

    
    response = llm.invoke([SystemMessage(content="You are a helpful AI assistant. Use natural, clear and easy-to-understand English."),
                *messages])

    return {'messages': [response]}


conn = sqlite3.connect(database="langgraph_chatbot.db",check_same_thread=False)
checkpoint = SqliteSaver(conn=conn)

graph = StateGraph(ChatbotState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")

graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpoint)


              

