from pymongo import MongoClient
from flask import current_app, g
from app.config import Config 

def get_db():
    """
    Get database connection from Flask g object or create a new one
    """
    if 'mongo_client' not in g:
        g.mongo_client = MongoClient(current_app.config['MONGO_URI'])
        g.db = g.mongo_client[current_app.config['MONGO_DB']]
    
    return g.db

def get_db_connection():
    """
    Get a database connection (for use outside Flask context)
    """
    mongo_client = MongoClient(Config.MONGO_URI)  
    db = mongo_client[Config.MONGO_DB]  
    return mongo_client, db

def init_db(app):
    """
    Initialize database connection with the Flask app
    """
    # Validate connection when the app starts
    try:
        client = MongoClient(app.config['MONGO_URI'])
        # Send a ping to confirm connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise
