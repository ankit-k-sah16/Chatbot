import streamlit as st

from backend1 import chatbot
from langchain.messages import HumanMessage

# st.session_state -> dict type -> refreshes when the page is manually refreshed.

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Loading conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type your message here...")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

if user_input :

    # Add user message to message history
    st.session_state['message_history'].append({"role": "user", "content": user_input})

    
    with st.chat_message("user"):
        st.text(user_input)

    # Generate response
   
    response = chatbot.invoke({ 'messages': [HumanMessage(content = user_input)]},config=config)
    ai_message = response['messages'][-1].content
     # Add assistant response to message history
    st.session_state['message_history'].append({'role':'assistant','content': ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)