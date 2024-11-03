# PASOS

1. crear el ambiente virtual: python -m venv venv
2. crea tu variable de ambiente ".env" en la raiz del proyecto, dentro especifica la url de tu base de datos "MONGO_URI= tu_url"
3. trabajar en el entorno virutal: ./venv/Scripts/activate
4. instalar librerias: pip install -r requirements.txt
5. poblar base de datos: python src/poblar_db.py
6. correr aplicación: python src/app.py
