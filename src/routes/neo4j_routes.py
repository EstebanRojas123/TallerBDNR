from flask import Blueprint, jsonify, request
from services.neo4j_service import add_rating, add_comment, sync_courses, get_courses, sync_users, get_people
import requests

neo4j_bp = Blueprint('neo4j', __name__)

@neo4j_bp.route('/add-rating', methods=['POST'])
def add_rating_route():
    data = request.get_json()
    username = data.get('username')
    course_id = data.get('course_id')
    rating = data.get('rating')

    if not username or not course_id or rating is None:
        return jsonify({"message": "username, course_id y rating son requeridos"}), 400

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"message": "La rating debe ser un entero entre 1 y 5"}), 400

    add_rating(username, course_id, rating)
    return jsonify({"message": "Valoración creada exitosamente"}), 201

@neo4j_bp.route('/add-comment', methods=['POST'])
def add_comment_route():
    data = request.get_json()
    username = data.get('username')
    course_id = data.get('course_id')
    title = data.get('title')
    details = data.get('details')

    if not username or not course_id or not title or not details:
        return jsonify({"message": "username, course_id, title, y details son requeridos"}), 400

    comentario_id = add_comment(username, course_id, title, details)

    courses_api_url = f"http://localhost:5000/courses/{course_id}/comment"
    try:
        response = requests.post(courses_api_url, json={"comentario_id": comentario_id})
        if response.status_code != 200:
            return jsonify({"message": "Comentario registrado en Neo4j, pero falló la actualización del curso en el sistema externo"}), 502
    except requests.RequestException as e:
        return jsonify({"message": f"Comentario registrado en Neo4j, pero ocurrió un error en la actualización del curso: {str(e)}"}), 502

    return jsonify({"message": "Comentario creado exitosamente", "comentario_id": comentario_id}), 201

@neo4j_bp.route('/sync-courses', methods=['POST'])
def sync_courses_route():
    MONGO_COURSES_URL = "http://localhost:5000/courses"

    try:
        response = requests.get(MONGO_COURSES_URL)
        response.raise_for_status()

        cursos = response.json().get('cursos', [])
        sync_courses(cursos)
        return jsonify({"message": "Sincronización completada exitosamente."}), 201
    except requests.RequestException as e:
        return jsonify({"message": "Error al obtener los cursos de MongoDB.", "error": str(e)}), 500

@neo4j_bp.route('/get-courses', methods=['GET'])
def get_courses_route():
    return jsonify(get_courses())

@neo4j_bp.route('/sync-users', methods=['POST'])
def sync_users_route():
    DYNAMODB_USERS_URL = "http://localhost:5000/dynamodb/users"

    try:
        response = requests.get(DYNAMODB_USERS_URL)
        response.raise_for_status()

        usuarios = response.json()
        sync_users(usuarios)
        return jsonify({"message": "Sincronización de usuarios completada exitosamente."}), 201
    except requests.RequestException as e:
        return jsonify({"message": "Error al obtener los usuarios de la base de datos.", "error": str(e)}), 500

@neo4j_bp.route('/get-people', methods=['GET'])
def get_people_route():
    return jsonify(get_people())
