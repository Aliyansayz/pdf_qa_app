import os
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index import download_loader




# from langchain.document_loaders import UnstructuredHTMLLoader
# from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import DirectoryLoader
from langchain.chains.question_answering import load_qa_chain

from langchain.schema import Document 
import pandas as pd
import requests
import pinecone
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
import numpy as np
import re

# ____________________________________________
# WILL BE USED IN FLASK APP IN FRONT END 

# host: https://arabic-bot-74438d8.svc.gcp-starter.pinecone.io
pinecone_environment = "gcp-starter"
pinecone_index_name  = "arabic-bot"
pinecoy_api_key = "83ffe0ca-4d89-4d5e-9a46-75bf76d6106f"

embeddings = OpenAIEmbeddings(model_name="ada")
unique_id  = "aaa365fe031e4b5ab90aba54eaf6012e"

# if len(messages) == 0 :  
#     relevant_docs = get_relevant_docs(query, embeddings, unique_id, final_doc_list )
#     qa_chain = define_qa(relevant_docs)
# else : 
#     relevant_docs = get_relevant_docs(query, final_doc_list = None) 
  
# answer = get_answer(query, qa_chain, relevant_docs)


messages.append( { "sender": f"{query}", "response": f"{answer}"   }  ) 

#  for message in messages: 
        # message.sender
        # message.response

def get_relevant_docs(query, embeddings, unique_id, final_doc_list = None ):
  
  document_count = 3
  
  if final_doc_list:
      try:
              push_to_pinecone(pinecoy_api_key, pinecone_environment, pinecone_index_name, embeddings,  final_docs_list) 
              relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings, unique_id )
      except:
              relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings, unique_id )
 
  else :
      relevant_docs = similar_docs(query, document_count ,"ad12a7c3-b36f-4b48-986e-5157cca233ef","gcp-starter","resume-db",embeddings, unique_id )
  
  return  relevant_docs
   
  # names =  metadata_filename(relevant_docs )
  # scores = get_score(relevant_docs)
  # content = docs_content(relevant_docs)
  
  # answer = get_answer(query, qa)
  # return answer 
# ____________________________________________

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationSummaryMemory



def get_answer(query, qa_chain, relevant_docs ):
    
    qa =  load_qa_chain(llm, chain_type="stuff")
    
    result = qa(query)
    answer =  qa_chain.run(input_documents=relevant_docs,
     question=query)
    
    return answer


   # similar_docs = get_similiar_docs(query)
   # answer = qa_chain.run(input_documents=similar_docs, question=query)


def get_api(hexcode):
    
 
    bytes_string = bytes.fromhex(hexcode)

    decoded_string = bytes_string.decode("utf-8")
    return  decoded_string
    


def define_qa(): 
       
     model_name = "text-davinci-003"
     # model_name = "gpt-3.5-turbo"
     # model_name = "gpt-4"
     llm = OpenAI(model_name=model_name)

     qa_chain =load_qa_chain(llm, chain_type="stuff")
    
     return qa_chain 


# directory = '/content/data'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents


def split_docs(documents, chunk_size=1000, chunk_overlap=0):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

# PDF UPLOAD --> INTO TEXT DOCUMENT --> EMBEDDING FUNCTION -->  PUSH INTO PINECONE WITH THEIR EMBEDDINGS

# DOCUMENTS TO MATCH = 3

# QUERY MATCH --> SIMILAR SEARCH --> RELEVANT DOCS --> RELEVANT DOCS INTO SUMMARY 

def create_docs(user_file_list, unique_id):
  pdfloader = PDFReader()
  user_file_list = os.listdir(directory)
  docs = []
  for filename in user_file_list:

      ext = filename.split(".")[-1]


      # Use PDFLoader for .pdf files
      if ext == "pdf":
          loader = PyPDFLoader(filename)
          doc = loader.load()

      
      # Skip other file types
      else:
          continue
      docs.append(Document( page_content= doc[0].page_content , metadata={"name": f"{filename}" , "unique_id":unique_id } ) )

  return docs



def create_docs_for_flask_web(directory, unique_id):

  pdfloader = PDFReader()
  user_file_list = os.listdir(directory)
  docs = []

  for filename in user_file_list:
    
      filepath = os.path.join(directory, filename)
      ext = filename.split(".")[-1]

      # Use PDFLoader for .pdf files
      if ext == "pdf":
          
          doc = pdfloader.load_data(file=Path(f'{filepath}'))
          # loader = PyPDFLoader(filepath)
          return doc
      else:
          continue
      docs.append(Document( page_content= doc[0].page_content , metadata={"name": f"{filename}" , "unique_id":unique_id } ) )

  return docs



def create_docs_not_working(directory, unique_id):
  
  user_file_list = os.listdir(directory)
  docs = []

  for filename in user_file_list:
    
      filepath = os.path.join(directory, filename)
      ext = filename.split(".")[-1]

      # Use PDFLoader for .pdf files
      if ext == "pdf":
          loader = PyPDFLoader(filepath)
          doc = loader.load()

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


