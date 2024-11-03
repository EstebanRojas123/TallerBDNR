from config.mongodb import mongo
from flask import request, jsonify, Response
from bson import json_util, ObjectId




def get_users_service():  # Obtener todos los usuarios
    data = mongo.db.users.find()
    users = []
    for user in data:
        user['_id'] = str(user['_id']) 
        users.append(user)
    
    return jsonify({'users': users})  



def create_user_service():   #crear un usuario  
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    admin = data.get('admin', None)
    
    if username is None or password is None or admin is None:
        print("dentro del if")
        return jsonify({'error': 'Faltan datos necesarios'}), 400

    new_user = {
        "username": username,
        "password": password,
        "admin": admin
    }
    
    result = mongo.db.users.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)
    
    return jsonify({'message': 'Usuario creado correctamente', "user":new_user}), 201
