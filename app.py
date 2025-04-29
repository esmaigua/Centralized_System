from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

app = Flask(__name__)
load_dotenv()  # Carga las variables desde .env

def get_connection():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise Exception("DATABASE_URL no está definida")

    result = urlparse(url)

    return psycopg2.connect(
        dbname=result.path[1:],  # Elimina el '/' inicial
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM usuarios LIMIT 1;")
    nombre = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return f"<h1>Hola Mundo</h1><p>Bienvenido, {nombre}.</p>"

if __name__ == "__main__":
    app.run(debug=True)

