import psycopg2
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


def test_connexion_postgres():
    try:
        # Récupérer les variables d'environnement
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DATABASE"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        print("Connexion réussie à PostgreSQL !")
        conn.close()
    except Exception as e:
        print(f"Erreur de connexion à PostgreSQL : {e}")


# Appeler la fonction de test
test_connexion_postgres()
