import streamlit as st
from response import *


st.title('Smart Tourist')

if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

st.markdown("""
<style>
.user-message {
text-align: left;
margin: 5px;
padding: 5px;
background-color: #f0f0f0; /* Light grey background for user message /
border-radius: 5px;
}
.reply-message {
text-align: right;
margin: 5px;
padding: 5px;
background-color: #d0d0d0; / Slightly darker grey for reply message */
border-radius: 5px;
}
.send-button {
width: 36px;
height: 36px;
padding: 0;
border-radius: 18px;
line-height: 0;
display: inline-block;
text-align: center;
vertical-align: middle;
margin-top: 30px;
}
.stTextInput > div > div > input {
padding-right: 40px;
}
</style>
""", unsafe_allow_html=True)
Function to handle text input and send button

def handle_input():
    user_input = st.session_state.user_input
    if user_input:
    # Append user query and reply to chat history
    answer = get_answer(query = input, qa_chain= qa_chain)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("reply", f"Ans: {answer}" ))
    # Clear the input box
    st.session_state.user_input = ""

chat_container = st.empty()
with chat_container.container():
    for message_type, message in st.session_state.chat_history:
      if message_type == "user":
          st.markdown(f'
          {message}
          ', unsafe_allow_html=True)
      elif message_type == "reply":
          st.markdown(f'
          {message}
          ', unsafe_allow_html=True)


col1, col2 = st.columns([5, 1], gap="small")
with col1:
      user_input = st.text_input("Ask me anything about tourism!",
      key="user_input",
      value="",
      on_change=handle_input,
      args=())
with col2:
      st.markdown('🠕', unsafe_allow_html=True)
