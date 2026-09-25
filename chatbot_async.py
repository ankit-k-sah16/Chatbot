from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode,tools_condition
from dotenv import load_dotenv
import sqlite3
import requests
import asyncio

load_dotenv()  # Load environment variables from .env file
#-------------------------------------------------
# 1. LLM Setup
#-------------------------------------------------

llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0.6)

#-------------------------------------------------
# 2. Tool Setup
#-------------------------------------------------

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

tools=[calculator_tool]

llm_with_tool = llm.bind_tools(tools)

#-------------------------------------------------
# 3. State Setup
#-------------------------------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_graph():

    async def chat_node(state: ChatState):

        "LLM node that answers the user query by ownself or using the given tools"
        messages = state['messages']
        response = await  llm_with_tool.ainvoke(messages)
        return {'messages':response}

    t_node = ToolNode(tools)

    #-------------------------------------------------
    # 5. Graph Setup
    #-------------------------------------------------
    graph = StateGraph(ChatState)
    graph.add_node('chat_node',chat_node)
    graph.add_node('tools',t_node)

    graph.add_edge(START,'chat_node')
    graph.add_conditional_edges('chat_node', tools_condition)

    graph.add_edge('tools','chat_node')

    chatbot = graph.compile()
    return chatbot

async def main():

    chatbot = build_graph()

    # running the graph
    result = await chatbot.ainvoke({"messages": [HumanMessage(content="Find the modulus of 132354 and 23 and give answer like a cricket commentator")]})

    print(result['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())