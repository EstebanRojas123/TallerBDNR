# PASOS

1. crear el ambiente virtual: python -m venv venv
2. Modificar en la variable de ambiente ".env" la url de su base de datos "MONGO_URI","NEO4J_USER","NEO4J_PASSWORD"
3. trabajar en el entorno virutal: ./venv/Scripts/activate
4. instalar librerias: pip install -r requirements.txt
5. Crear tablas clave-valor: src/initialize.py
6. correr aplicación: python src/app.py

Nota: Al probar los endpoints que requieren un ID específico, verifica manualmente los identificadores (\_id), ya que se generan de forma aleatoria al poblar la base de datos.
Nota 2: DynamoDB esta usando el puerto por defecto: 8000.
