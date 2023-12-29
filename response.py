import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.chains.question_answering import load_qa_chain

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

embeddings = OpenAIEmbeddings(model_name="ada")
unique_id  = 

if len(messages) == 0 :  
    relevant_docs = get_relevant_docs(query, embeddings, unique_id, final_doc_list )
    qa_chain = define_qa(relevant_docs)
else : 
    relevant_docs = get_relevant_docs(query, final_doc_list = None) 
  
answer = get_answer(query, qa_chain, relevant_docs)


messages.append( { "sender": f"{query}", "response": f"{answer}"   }  ) 

#  for message in messages: 
        # message.sender
        # message.response

def get_relevant_docs(query, embeddings, unique_id, final_doc_list = None ):
  
  document_count = 3
  
  if final_doc_list:
      try:
              push_to_pinecone("ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings,final_docs_list) 
              relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings,st.session_state['unique_id'])
      except:
              relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings,st.session_state['unique_id'])
 
  else :
      relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings,st.session_state['unique_id'])
  
  return  relevant_docs
   
  # names =  metadata_filename(relevant_docs )
  # scores = get_score(relevant_docs)
  # content = docs_content(relevant_docs)
  
  answer = get_answer(query, qa)
  return answer 
# ____________________________________________

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory



def get_answer(query, qa_chain, relevant_docs ):
    
    qa =  load_qa_chain(llm, chain_type="stuff")
    
    result = qa(query)
    answer =  qa_chain.run(input_documents=relevant_docs,
     question=query)
    return answer


   similar_docs = get_similiar_docs(query)
  answer = qa_chain.run(input_documents=similar_docs, question=query)



def define_qa(): 
     
     
     model_name = "text-davinci-003"
     # model_name = "gpt-3.5-turbo"
     # model_name = "gpt-4"
     llm = OpenAI(model_name=model_name)
     chain = load_qa_chain(llm, chain_type="stuff")

     llm = ChatOpenAI(model_name="gpt-3.5-turbo")
     qa_chain =load_qa_chain(llm, chain_type="stuff")
    
     return qa_chain 


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


