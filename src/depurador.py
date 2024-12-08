from pymongo import MongoClient
import os

mongo_uri = os.getenv('MONGO_URI')  
try:
    client = MongoClient(mongo_uri)
    client.admin.command('ping')
    print("Conexión a MongoDB exitosa.")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
