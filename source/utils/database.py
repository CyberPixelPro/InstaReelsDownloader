from pymongo import MongoClient
import config

client = MongoClient(config.MONGODB_URI)
db = client['InstagramReels']

def add_user(user_id, username):
    users_collection = db['users']
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"username": username}},
        upsert=True
    )

def add_chat(chat_id, chat_title):
    chats_collection = db['chats']
    chats_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"title": chat_title}},
        upsert=True
    )

def get_all_users():
    users_collection = db['users']
    return list(users_collection.find({}))

def get_all_chats():
    chats_collection = db['chats']
    return list(chats_collection.find({}))
