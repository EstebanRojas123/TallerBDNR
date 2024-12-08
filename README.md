# PASOS

1. crear el ambiente virtual: python -m venv venv
2. Modificar en la variable de ambiente ".env" la url de su base de datos "MONGO_URI = URL"
3. trabajar en el entorno virutal: ./venv/Scripts/activate
4. instalar librerias: pip install -r requirements.txt
5. correr aplicación: python src/app.py

Nota: Al probar los endpoints que requieren un ID específico, verifica manualmente los identificadores (_id), ya que se generan de forma aleatoria al poblar la base de datos.
