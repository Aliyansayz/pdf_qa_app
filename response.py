import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.schema import Document 
import pandas as pd
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
import requests
import pinecone
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
import numpy as np
import re

# ____________________________________________
WILL BE USED IN FLASK APP IN FRONT END 

answer = save_answer(query, final_doc_list = None )

messages.append( { "sender": f"{query}", "response": f"{answer}"   }  ) 

#  for message in message: 
        # message.sender
        # message.response

def save_answer(query, final_doc_list = None ):
  if final_doc_list:

      push_to_pinecone("ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings,final_docs_list) 
      document_count = 3
      relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings,st.session_state['unique_id'])
  else :
      relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings,st.session_state['unique_id'])
    
  # names =  metadata_filename(relevant_docs )
  # scores = get_score(relevant_docs)
  # content = docs_content(relevant_docs)
  
  answer = get_answer(query, relevant_docs)
  return answer 
# ____________________________________________

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory

def get_answer(query, relevant_docs):
    
    llm = ChatOpenAI(model_name="gpt-4")
    memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    result = qa(question)
  
    return result["answer"]


# PDF UPLOAD --> INTO TEXT DOCUMENT --> EMBEDDING FUNCTION -->  PUSH INTO PINECONE WITH THEIR EMBEDDINGS

# DOCUMENTS TO MATCH = 3

# QUERY MATCH --> SIMILAR SEARCH --> RELEVANT DOCS --> RELEVANT DOCS INTO SUMMARY 

def create_docs(user_file_list, unique_id):
  docs = []
  for filename in user_file_list:

      ext = filename.split(".")[-1]

      # Use PDFLoader for .pdf files
      if ext == "pdf":
          loader = PyPDFLoader(filename)
          doc = loader.load()

      elif ext == "docx":
          loader = Docx2txtLoader(filename)
          doc = loader.load()

      elif ext == "md":
          loader = UnstructuredMarkdownLoader(filename)
          doc = loader.load()
      # Skip other file types
      else:
          continue
      docs.append(Document( page_content= doc[0].page_content , metadata={"name": f"{filename}" , "unique_id":unique_id } ) )

  return docs


def docs_content(relevant_docs):
    content = [] 
    for doc in relevant_docs:    
        content.append(doc[0].page_content)

    return content



#Create embeddings instance
def create_embeddings_load_data():
    #embeddings = OpenAIEmbeddings()
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") #  384
    return embeddings


#Function to push data to Vector Store - Pinecone here
def push_to_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,docs):

    pinecone.init(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )
    print("done......2")
    Pinecone.from_documents(docs, embeddings, index_name=pinecone_index_name)
    


def pull_from_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings):

    pinecone.init(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )

    index_name = pinecone_index_name

    index = Pinecone.from_existing_index(index_name, embeddings)
    return index

def get_score(relevant_docs):
  scores = []
  for doc in relevant_docs:
      scores.append(doc[1])

  return scores


def metadata_filename( document ) : 
   
   names = [ ]
   for doc in document: 
    
        text = str(doc[0].metadata["name"] )
        pattern = r"name=\'(.*?)\'"
        matches = re.findall(pattern, text)
        names.append(matches) 

   return names


