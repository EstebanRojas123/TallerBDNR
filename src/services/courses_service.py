from config.mongodb import mongo
from flask import request, jsonify,Response
from bson import ObjectId, json_util
from services.units_service import get_units_by_ids


def create_course_service():
    data = request.get_json()
    
    new_course = {
        "nombre": data["nombre"],
        "descripcion": data["descripcion"],
        "imagen_principal": data["imagen_principal"],
        "imagen_detalle": data["imagen_detalle"],
        "valoraciones": [],
        "valoracion_promedio": 0,
        "comentarios": [],
        "participantes": 0,
        "unidades": [],
        "inscritos": []
    }
    
    course_id = mongo.db.curso.insert_one(new_course).inserted_id

    unidades_ids = []
    for unidad in data["unidades"]:
        new_unit = {
            "nombre": unidad["nombre"],
            "orden": unidad["orden"],
            "curso_id": course_id,
            "clases": []
        }
        
        unit_id = mongo.db.unidad.insert_one(new_unit).inserted_id
        unidades_ids.append(unit_id)

        clases_ids = []
        for clase in unidad["clases"]:
            new_class = {
                "nombre": clase["nombre"],
                "descripcion": clase["descripcion"],
                "video_url": clase["video_url"],
                "archivos_adjuntos": clase["archivos_adjuntos"],
                "orden": clase["orden"],
                "comentarios": [],
                "unidad_id": unit_id
            }

            class_id = mongo.db.clase.insert_one(new_class).inserted_id
            clases_ids.append(class_id)

        mongo.db.unidad.update_one(
            {"_id": unit_id},
            {"$set": {"clases": clases_ids}}
        )

    mongo.db.curso.update_one(
        {"_id": course_id},
        {"$set": {"unidades": unidades_ids}}
    )

    return jsonify({"message": "Curso creado exitosamente", "course_id": str(course_id)}), 201

def get_all_courses_service():
    courses = mongo.db.curso.find({}, {
        "nombre": 1,
        "imagen_principal": 1,
        "descripcion": 1,
        "valoraciones": 1,
        "valoracion_promedio": 1,
        "comentarios": 1
    })

    course_list = []
    for course in courses:
        course["_id"] = str(course["_id"])

        if "comentarios" in course:
            for i, comentario in enumerate(course["comentarios"]):
                if isinstance(comentario, ObjectId):
                    course["comentarios"][i] = str(comentario)
                elif isinstance(comentario, dict):
                    if "_id" in comentario and isinstance(comentario["_id"], ObjectId):
                        comentario["_id"] = str(comentario["_id"])

        course_list.append(course)

    return jsonify({"cursos": course_list}), 200

def get_course_by_id(id):
    course = mongo.db.curso.find_one({"_id": ObjectId(id)})
    
    if course is None:
        return jsonify({"error": "Curso no encontrado"}), 404

    unit_ids = course.get("unidades", [])
    course["unidades"] = get_units_by_ids(unit_ids)

    return Response(json_util.dumps(course), mimetype="application/json"), 200

def register_user_in_course(course_id, user_id):
    course = mongo.db.curso.find_one({"_id": ObjectId(course_id)})

    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404


    if user_id in course.get("inscritos", []):
        return jsonify({"message": "Usuario ya está registrado en el curso"}), 200

    mongo.db.curso.update_one(
        {"_id": ObjectId(course_id)},
        {
            "$push": {"inscritos": user_id},
            "$inc": {"participantes": 1} 
        }
    )

    return jsonify({"message": "Usuario registrado correctamente"}), 200

def add_course_rating_service(course_id):
    data = request.get_json()
    valoracion = data.get("valoracion")

    if valoracion is None or not isinstance(valoracion, (int, float)) or not (0 <= valoracion <= 5):
        return jsonify({"error": "La valoración debe ser un número entre 0 y 5."}), 400

    course = mongo.db.curso.find_one({"_id": ObjectId(course_id)})

    if not course:
        return jsonify({"error": "Curso no encontrado."}), 404

    mongo.db.curso.update_one(
        {"_id": ObjectId(course_id)},
        {"$push": {"valoraciones": valoracion}}
    )

    valoraciones_actualizadas = course.get("valoraciones", []) + [valoracion]
    valoracion_promedio = sum(valoraciones_actualizadas) / len(valoraciones_actualizadas)

    mongo.db.curso.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": {"valoracion_promedio": valoracion_promedio}}
    )

    return jsonify({"message": "Valoración agregada correctamente.", "valoracion_promedio": valoracion_promedio}), 200

def add_course_comment_service(course_id):
    data = request.get_json()
    comentario_id = data.get("comentario_id")

    if not comentario_id or not isinstance(comentario_id, str):
        return jsonify({"error": "Se requiere un comentario_id válido."}), 400

    course = mongo.db.curso.find_one({"_id": ObjectId(course_id)})

    if not course:
        return jsonify({"error": "Curso no encontrado."}), 404

    mongo.db.curso.update_one(
        {"_id": ObjectId(course_id)},
        {"$push": {"comentarios": comentario_id}}
    )

    return jsonify({"message": "Comentario agregado correctamente."}), 200
