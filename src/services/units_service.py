from bson import ObjectId
from flask import jsonify
from config.mongodb import mongo

def get_units_by_ids(unit_ids):
    units = list(mongo.db.unidad.find({"_id": {"$in": [ObjectId(unit_id) for unit_id in unit_ids]}}))
    
  
    for unit in units:
        unit["_id"] = str(unit["_id"])
    
        return units



def get_classes_by_unit_id(unit_id):
    unit = mongo.db.unidad.find_one({"_id": ObjectId(unit_id)}, {"clases": 1})
    
    if not unit:
        return jsonify({"error": "Unidad no encontrada"}), 404


    class_ids = unit.get("clases", [])


    classes = list(mongo.db.clase.find(
        {"_id": {"$in": [ObjectId(class_id) for class_id in class_ids]}},
        {"nombre": 1}
    ))

    for cls in classes:
        cls["_id"] = str(cls["_id"])

    return jsonify({"clases": classes}), 200