from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from pymongo import MongoClient
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
import os
import faiss
import numpy as np
import sys
from dotenv import load_dotenv

load_dotenv("variables.env")


def get_embedding_data_mongo():
    client = MongoClient(os.environ.get('MONGO_URI' ))
    db = client[os.environ.get ('DB')]
    collection = db[os.environ.get ("embedding_COLLECTIONS")]
    
    documents = []
    embedding_list = []
    for doc in collection.find():
        text = doc["text"]
        embedding = np.array(doc["embedding"], dtype=np.float32)
        documents.append(Document(page_content=text, metadata=doc.get("metadata", {})))
        embedding_list.append(embedding)
        return documents,embedding_list

embedding_model = OllamaEmbeddings(model="nomic-embed-text")
dimension = 768
index = faiss.IndexFlatL2(dimension)

documents,embedding_list=get_embedding_data_mongo()
embedding_array = np.array(embedding_list).astype(np.float32)
index.add(embedding_array)
index_to_docstore_id = {i: str(i) for i in range(len(documents))}
docstore = {str(i): doc for i, doc in enumerate(documents)}  # Convert documents to dictionary

vectorstore = FAISS.from_documents(
    documents, embedding_model)


def chatbot_query(query):
    template = """
    Question: {question}

    Answer: Let's think step by step.
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.2", temperature=0)

    retriever = vectorstore.as_retriever()

    retriever_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        chain_type="stuff"
    )
    sys.stdout.write("Let me think for a moment...\r")
    sys.stdout.flush()



    return retriever_chain({"query": query})
