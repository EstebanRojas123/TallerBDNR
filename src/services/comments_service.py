from config.mongodb import mongo
from flask import request, jsonify
from bson import ObjectId
from datetime import datetime


def create_comment_service(entity_type, entity_id):
    data = request.get_json()

    # Crear el comentario
    new_comment = {
        "title": data["title"],
        "id_user": data["id_user"],
        "content": data["content"],
        "likes": data.get("likes", 0),
        "dislikes": data.get("dislikes", 0),
        "fecha": datetime.utcnow(),  
        "entity_type": entity_type, 
        "entity_id": entity_id  
    }

    
    comment_id = mongo.db.comentarios.insert_one(new_comment).inserted_id

   
    if entity_type == "curso":
        mongo.db.curso.update_one(
            {"_id": ObjectId(entity_id)},
            {"$push": {"comentarios": str(comment_id)}}
        )
    elif entity_type == "clase":
        mongo.db.clase.update_one(
            {"_id": ObjectId(entity_id)},
            {"$push": {"comentarios": str(comment_id)}}
        )

    return jsonify({"message": "Comentario creado exitosamente", "comment_id": str(comment_id)}), 201
