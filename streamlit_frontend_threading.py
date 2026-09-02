import streamlit as st
from backend1 import chatbot
from langchain.messages import HumanMessage
import uuid

# ********************************* Utility Functions *******************************************

# Generates a unique thread ID for each new chat session
def generate_thread_id():
    thread_id = uuid.uuid4()

    return str(thread_id)

# Resets the chat session by clearing the message history and generating a new thread ID
def reset_chat():
    thread_id = generate_thread_id()

    st.session_state['thread_id'] = thread_id

    add_thread_to_history(st.session_state['thread_id'])

    st.session_state['message_history'] = []

# Adds a thread ID to the history of chat threads
def add_thread_to_history(thread_id):

    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

#
def load_conversation_history(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    return state.values.get("messages", [])

# ********************************* Session Setup ***********************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_thread_to_history(st.session_state['thread_id'])

# ********************************* Sidebar UI **************************************************

st.sidebar.title("Chatbot")

st.sidebar.button("New Chat",on_click=reset_chat, type="primary")

st.sidebar.header("Previous Conversations")

for thread_id in st.session_state['chat_threads'][::-1 ]:  # Display threads in reverse order (most recent first)

    if st.sidebar.button(thread_id):

        st.session_state['thread_id'] = thread_id

        messages = load_conversation_history(thread_id)

        temp_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):
                role = 'user'

            else:
                role = 'assistant'
            
            temp_messages.append({"role": role, "content": message.content})

        st.session_state['message_history'] = temp_messages
        st.rerun()  # Refresh the app to display the loaded conversation


# ********************************* Main UI ******************************************************

# Loading conversation history
for message in st.session_state['message_history']:

    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Chat Input

user_input = st.chat_input("Type your message here...")


if user_input :

    # Adding user message to UI history
    st.session_state['message_history'].append({"role": "user", "content": user_input})

    
    with st.chat_message("user"):
        st.markdown(user_input)

    CONFIG ={ "configurable": {"thread_id": st.session_state['thread_id'] }}


    # Response Generation
    with st.chat_message("assistant"):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream(
            { 'messages': [HumanMessage(content = user_input)]},
            config = CONFIG,
            stream_mode = "messages"
        )
    )
        
    # Adding assistant response to UI history
    st.session_state['message_history'].append({"role": "assistant", "content": ai_message})