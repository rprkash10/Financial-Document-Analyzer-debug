import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# --- Database Connection ---
client = None
db = None

def connect_to_db():
    global client, db
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise Exception("MONGO_URI environment variable not set.")
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.financial_analyzer_db
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def get_db():
    if db is None:
        connect_to_db()
    return db

# --- Function to Save Analysis ---
def save_analysis(query: str, file_name: str, analysis_result: str):
    database = get_db()
    collection = database.analysis_results
    document = {
        "query": query,
        "file_name": file_name,
        "analysis": analysis_result,
        "timestamp": datetime.datetime.now(datetime.UTC)
    }
    return collection.insert_one(document).inserted_id