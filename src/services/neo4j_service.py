from config.neo4j_config import get_driver

def add_rating(username, course_id, rating):
    """Agrega una valoración para un curso"""
    with get_driver().session() as session:
        session.run("""
            MATCH (u:User {username: $username}), (c:Curso {id: $course_id})
            CREATE (u)-[:VALORÓ]->(val:Valoracion {valor: $rating})
            CREATE (val)-[:SOBRE]->(c)
        """, username=username, course_id=course_id, rating=rating)

def add_comment(username, course_id, title, details):
    """Agrega un comentario a un curso"""
    with get_driver().session() as session:
        result = session.run("""
            MATCH (u:User {username: $username}), (c:Curso {id: $course_id})
            CREATE (com:Comentario {titulo: $title, detalles: $details})
            CREATE (u)-[:COMENTÓ]->(com)
            CREATE (com)-[:SOBRE]->(c)
            RETURN ID(com) AS comentario_id
        """, username=username, course_id=course_id, title=title, details=details)
        return result.single()["comentario_id"]

def sync_courses(courses):
    """Sincroniza cursos desde MongoDB a Neo4j"""
    with get_driver().session() as session:
        for curso in courses:
            course_id = curso.get('_id')
            course_name = curso.get('nombre')

            if not course_id or not course_name:
                continue

            result = session.run("MATCH (c:Curso {id: $id}) RETURN c", id=course_id)
            if result.single():
                continue

            session.run("CREATE (c:Curso {id: $id, nombreDelCurso: $nombreDelCurso})", id=course_id, nombreDelCurso=course_name)

def get_courses():
    """Obtiene todos los cursos almacenados en Neo4j"""
    with get_driver().session() as session:
        result = session.run("MATCH (c:Curso) RETURN c.id AS id, c.nombreDelCurso AS nombreDelCurso")
        return [{"id": record["id"], "nombreDelCurso": record["nombreDelCurso"]} for record in result]

def sync_users(users):
    """Sincroniza usuarios desde DynamoDB a Neo4j"""
    with get_driver().session() as session:
        for usuario in users:
            username = usuario.get('username')

            if not username:
                continue

            result = session.run("MATCH (u:User {username: $username}) RETURN u", username=username)
            if result.single():
                continue

            session.run("CREATE (u:User {username: $username})", username=username)

def get_people():
    """Obtiene los usuarios de Neo4j"""
    with get_driver().session() as session:
        result = session.run("MATCH (p:User) RETURN p.name AS username, p.age AS id")
        return [{"username": record["username"], "id": record["id"]} for record in result]
