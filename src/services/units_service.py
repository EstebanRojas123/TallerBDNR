from bson import ObjectId
from flask import jsonify
from config.mongodb import mongo

def get_units_by_ids(unit_ids):
    # Devuelve todas las unidades que coincidan con los IDs dados
    units = list(mongo.db.unidad.find({"_id": {"$in": [ObjectId(unit_id) for unit_id in unit_ids]}}))
    
    # Convertir ObjectId a string para cada unidad
    for unit in units:
        unit["_id"] = str(unit["_id"])
    
    return units


# Nuevo método para obtener clases por ID de unidad
def get_classes_by_unit_id(unit_id):
    unit = mongo.db.unidad.find_one({"_id": ObjectId(unit_id)}, {"clases": 1})
    
    if not unit:
        return jsonify({"error": "Unidad no encontrada"}), 404

    # Extrae los IDs de las clases de la unidad
    class_ids = unit.get("clases", [])

    # Encuentra las clases en la colección `clase` y devuelve solo el nombre
    classes = list(mongo.db.clase.find(
        {"_id": {"$in": [ObjectId(class_id) for class_id in class_ids]}},
        {"nombre": 1}
    ))

    # Convertir ObjectId a string para cada clase
    for cls in classes:
        cls["_id"] = str(cls["_id"])

    return jsonify({"clases": classes}), 200