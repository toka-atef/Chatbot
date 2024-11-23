from pymongo import MongoClient
from langchain.document_loaders.csv_loader import CSVLoader
import os
from dotenv import load_dotenv

load_dotenv("assisment_scripts/variables.env")


def add_data_to_mongo():
    loader = CSVLoader(file_path=os.environ.get('csv_data_path'))
    data = loader.load()
    formatted_documents = [{"text": doc.page_content, "metadata": doc.metadata} for doc in data]
    # MongoDB connection URI
    client = MongoClient(os.environ.get('MONGO_URI'))
    db = client[os.environ.get ('DB')]
    collection = db[os.environ.get("Data_COLLECTIONS")]

    collection.insert_many(formatted_documents)
    print("Data Uploded to Mongo Databas!!")

add_data_to_mongo()    