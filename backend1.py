from langchain_groq import ChatGroq

from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages


from langgraph.checkpoint.memory import InMemorySaver
env = load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b")

class ChatbotState(TypedDict):

    messages: Annotated[list['BaseMessage'], add_messages]


def chat_node(state: ChatbotState):

    messages = state['messages']

    
    response = llm.invoke([SystemMessage(content="You are a helpful AI assistant. Use natural, clear and easy-to-understand English."),
                *messages])

    return {'messages': [response]}

checkpoint = InMemorySaver()

graph = StateGraph(ChatbotState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")

graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpoint)


              

