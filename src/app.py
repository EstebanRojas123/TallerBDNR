from flask import Flask, jsonify
from neo4j import GraphDatabase
from flask import request
import datetime 
from flask import Flask, render_template
from dotenv import load_dotenv
import os
from flask_cors import CORS
from config.mongodb import mongo
from config.initialize_db import initialize_database
from routes.users_routes import users
from routes.courses_routes import courses 
from routes.units_routes import units
from routes.class_routes import classes
from poblar_db import populate_database
from routes.dynamodb_routes import dynamodb_bp
import requests

load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)
CORS(app)

app = Flask(__name__)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = ""
NEO4J_PASSWORD = ""

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.route('/neo4j/add-rating', methods=['POST'])
def add_rating():
    data = request.get_json()
    username = data.get('username')
    course_id = data.get('course_id')
    rating = data.get('rating')

    if not username or not course_id or rating is None:
        return jsonify({"message": "username, course_id y rating son requeridos"}), 400

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"message": "La rating debe ser un entero entre 1 y 5"}), 400

    with driver.session() as session:
        session.run("""
            MATCH (u:User {username: $username}), (c:Curso {id: $course_id})
            CREATE (u)-[:VALORÓ]->(val:Valoracion {valor: $rating})
            CREATE (val)-[:SOBRE]->(c)
            """, username=username, course_id=course_id, rating=rating)

    return jsonify({"message": "Valoración creada exitosamente"}), 201

@app.route('/neo4j/add-comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    username = data.get('username')
    course_id = data.get('course_id')
    title = data.get('title')
    details = data.get('details')

    if not username or not course_id or not title or not details:
        return jsonify({"message": "username, course_id, title, y details son requeridos"}), 400

    comentario_id = None

    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {username: $username}), (c:Curso {id: $course_id})
            CREATE (com:Comentario {titulo: $title, detalles: $details})
            CREATE (u)-[:COMENTÓ]->(com)
            CREATE (com)-[:SOBRE]->(c)
            RETURN ID(com) AS comentario_id
            """, username=username, course_id=course_id, title=title, details=details)

        record = result.single()

        if record:
            comentario_id = str(record["comentario_id"])

    if comentario_id is None:
        return jsonify({"message": "Error al crear el comentario en Neo4j"}), 500

    courses_api_url = f"http://localhost:5000/courses/{course_id}/comment"
    try:
        response = requests.post(courses_api_url, json={"comentario_id": comentario_id})
        if response.status_code != 200:
            return jsonify({"message": "Comentario registrado en Neo4j, pero falló la actualización del curso en el sistema externo"}), 502
    except requests.RequestException as e:
        return jsonify({"message": f"Comentario registrado en Neo4j, pero ocurrió un error en la actualización del curso: {str(e)}"}), 502

    return jsonify({"message": "Comentario creado exitosamente", "comentario_id": comentario_id}), 201

@app.route('/neo4j/sync-courses', methods=['POST'])
def sync_courses():
    MONGO_COURSES_URL = "http://localhost:5000/courses"

    try:
        response = requests.get(MONGO_COURSES_URL)
        response.raise_for_status()
        
        cursos = response.json().get('cursos', [])
        
        if not cursos:
            return jsonify({"message": "No se encontraron cursos en la base de datos MongoDB."}), 404

        with driver.session() as session:
            for curso in cursos:
                course_id = curso.get('_id')
                course_name = curso.get('nombre')

                if not course_id or not course_name:
                    continue

                result = session.run(
                    "MATCH (c:Curso {id: $id}) RETURN c",
                    id=course_id
                )

                if result.single():
                    continue

                session.run(
                    "CREATE (c:Curso {id: $id, nombreDelCurso: $nombreDelCurso})",
                    id=course_id,
                    nombreDelCurso=course_name
                )

        return jsonify({"message": "Sincronización completada exitosamente."}), 201

    except requests.RequestException as e:
        return jsonify({"message": "Error al obtener los cursos de MongoDB.", "error": str(e)}), 500

@app.route('/neo4j/get-courses', methods=['GET'])
def get_courses():
    with driver.session() as session:
        result = session.run("MATCH (c:Curso) RETURN c.id AS id, c.nombreDelCurso AS nombreDelCurso")
        courses = [{"id": record["id"], "nombreDelCurso": record["nombreDelCurso"]} for record in result]
        return jsonify(courses)

@app.route('/neo4j/sync-users', methods=['POST'])
def sync_users():
    DYNAMODB_USERS_URL = "http://localhost:5000/dynamodb/users"

    try:
        response = requests.get(DYNAMODB_USERS_URL)
        response.raise_for_status()

        usuarios = response.json()

        if not usuarios:
            return jsonify({"message": "No se encontraron usuarios en la base de datos."}), 404

        with driver.session() as session:
            for usuario in usuarios:
                username = usuario.get('username')

                if not username:
                    continue

                result = session.run(
                    "MATCH (u:User {username: $username}) RETURN u",
                    username=username
                )

                if result.single():
                    continue

                session.run(
                    "CREATE (u:User {username: $username})",
                    username=username
                )

        return jsonify({"message": "Sincronización de usuarios completada exitosamente."}), 201

    except requests.RequestException as e:
        return jsonify({"message": "Error al obtener los usuarios de la base de datos.", "error": str(e)}), 500

@app.route('/neo4j/get-people', methods=['GET'])
def get_people():
    with driver.session() as session:
        result = session.run("MATCH (p:User) RETURN p.name AS username, p.age AS id")
        people = [{"username": record["username"], "id": record["id"]} for record in result]
        return jsonify(people)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(dynamodb_bp, url_prefix='/dynamodb')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(courses, url_prefix='/courses') 
app.register_blueprint(units, url_prefix='/units')
app.register_blueprint(classes, url_prefix='/classes')

if __name__ == '__main__':
    app.run(debug=True)
