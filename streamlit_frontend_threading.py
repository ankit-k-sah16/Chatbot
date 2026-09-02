import streamlit as st
from backend1 import chatbot
from langchain.messages import HumanMessage
import uuid

# ********************************* Utility Functions *******************************************

# Generate a unique thread ID for each new chat session
def generate_thread_id():
    thread_id = uuid.uuid4()

    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []


# ********************************* Session Setup ***********************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


# ********************************* Sidebar UI **************************************************

st.sidebar.title("LangGraph Chatbot")
st.sidebar.button("New Chat",on_click=reset_chat, type="primary")
st.sidebar.header("Previous Conversations")
#st.sidebar.text(st.session_state['message_history'][-1]['content'] if st.session_state['message_history'] else "No previous conversations.")
st.sidebar.text(st.session_state['thread_id'])

# ********************************* Main UI ******************************************************

# Loading conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type your message here...")


if user_input :

    # Adding user message to message history
    st.session_state['message_history'].append({"role": "user", "content": user_input})

    
    with st.chat_message("user"):
        st.text(user_input)

    CONFIG ={ "configurable": {"thread_id": st.session_state['thread_id'] }}
    # Response Generation
    with st.chat_message("assistant"):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream ({ 'messages': [HumanMessage(content = user_input)]},
            config = CONFIG,
            stream_mode = "messages"
        )
    )
    # Adding assistant response to message history
    st.session_state['message_history'].append({"role": "assistant", "content": ai_message})