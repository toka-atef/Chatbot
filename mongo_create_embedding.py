import numpy as np
import faiss
from pymongo import MongoClient
from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import os
from dotenv import load_dotenv

load_dotenv("variables.env")

client = MongoClient(os.environ.get('MONGO_URI'))
db = client[os.environ.get('DB')]

    

def pull_dataset():
    collection = db[os.environ.get ("Data_COLLECTIONS")]

    # Retrieve documents from MongoDB
    retrieved_docs = [doc for doc in collection.find()]

    # Convert documents to text data for embedding
    texts = [doc["text"] for doc in retrieved_docs]
    return texts

def generate_embedding(texts):
    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text",
    )
    # Generate embeddings for the text data
    print("Start embeddings")
    embeddings = [embedding_model.embed_query(text) for text in texts]
    embeddings_np = np.array(embeddings).astype(np.float32)

    # Create FAISS index
    index = faiss.IndexFlatL2(embeddings_np.shape[1]) 
    index.add(embeddings_np)  
    return embeddings,embeddings_np,index,embedding_model


def mongo_upload_embeddings(texts):
   
    embeddings,_,_,_= generate_embedding(texts)
    print("Start saving embeddings")
    collection = db[os.environ.get ("embedding_COLLECTIONS")]
    for i, text in enumerate(texts):
        # collection=db[os.environ.get ("embedding_COLLECTIONS")]
        embedding = np.array(embeddings[i]) if not isinstance(embeddings[i], np.ndarray) else embeddings[i]

        doc = {
            "text": text,
            "embedding": embedding.tolist(),
            "index": i  
        }
        
        collection.insert_one(doc)
    print("Embeddind Uploaded To MongoDB")

texts=pull_dataset()
mongo_upload_embeddings(texts)

