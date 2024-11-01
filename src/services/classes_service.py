from bson import ObjectId
from flask import jsonify
from config.mongodb import mongo

# Función para obtener el detalle de una clase por su ID
def get_class_by_id(class_id):
    # Busca la clase en la colección `clase` por su `_id`
    class_detail = mongo.db.clase.find_one({"_id": ObjectId(class_id)})
    
    if not class_detail:
        return jsonify({"error": "Clase no encontrada"}), 404

    # Convertir ObjectId a string en el resultado
    class_detail["_id"] = str(class_detail["_id"])
    class_detail["unidad_id"] = str(class_detail["unidad_id"])

    return jsonify({"clase": class_detail}), 200
