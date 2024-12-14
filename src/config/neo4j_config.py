from neo4j import GraphDatabase
import os
from dotenv import load_dotenv


load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not NEO4J_URI or not NEO4J_USER or not NEO4J_PASSWORD:
    raise ValueError("Faltan variables de entorno para la conexión a Neo4j. Verifica el archivo .env.")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_driver():
    """
    Devuelve la instancia del driver Neo4j.
    """
    return driver

def close_driver():
    """
    Cierra la conexión del driver Neo4j.
    """
    driver.close()
