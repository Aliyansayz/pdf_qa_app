import streamlit as st
from response import *
from dotenv import load_dotenv

load_dotenv()
st.title('Smart Tourist')

pinecone_environment = "gcp-starter"
pinecone_index_name  = "arabic-bot"
pinecone_api_key = "83ffe0ca-4d89-4d5e-9a46-75bf76d6106f"
unique_id = "aaa365fe031e4b5ab90aba54eaf6012e"
option = st.radio("Do you want to upload new resumes with this request ? ", ["Yes", "No" ]) 

# Display content based on the selected option
if option == "Yes":
# st.header("Resume ")
        documents = st.file_uploader("Upload resumes here : ", type=["pdf"],accept_multiple_files=True)
        if documents :
            st.success("File uploaded successfully!")
            embeddings=create_embeddings_load_data()
            final_docs_list=create_docs(resume ,st.session_state['unique_id'])    
            push_to_pinecone(pinecone_api_key, pinecone_environment, pinecone_index_name, embeddings,final_docs_list) 


global qa_chain
if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        qa_chain = define_qa()

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

def handle_input():
    user_input = st.session_state.user_input
    if user_input:
            # Append user query and reply to chat history
            relevant_docs = similar_docs(user_input,2,pinecone_api_key, pinecone_environment, pinecone_index_name, embeddings, unique_id )
            answer = get_answer(user_input, qa_chain, relevant_docs )
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
