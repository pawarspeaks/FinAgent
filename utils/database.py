from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB using the MONGO_URI environment variable
client = MongoClient(os.getenv("MONGO_URI"))
db = client["finagent360"]
individuals_collection = db["individuals"]
chat_history_collection = db["chat_history"]

def get_user(email):
    return individuals_collection.find_one({"email": email})

def create_user(user_data):
    return individuals_collection.insert_one(user_data)

def update_user(email, user_data):
    return individuals_collection.update_one({"email": email}, {"$set": user_data})

def verify_user(email, password):
    user = get_user(email)
    if user and user["password"] == password:
        return user
    return None

def save_chat_history(email, messages):
    chat_history_collection.update_one({"email": email}, {"$set": {"messages": messages}}, upsert=True)

def load_chat_history(email):
    chat_history = chat_history_collection.find_one({"email": email})
    if chat_history:
        return chat_history["messages"]
    return []
