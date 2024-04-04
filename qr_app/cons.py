import os
import sqlite3
import time
import hashlib, base64
from cryptography.fernet import Fernet

# Definir la ruta de la base de datos local
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local_database.db')

KEY = os.environ.get('EncryptKey')

# Generar la clave Fernet a partir de la clave fija
def generate_fernet_key():
    # Crear una clave de 32 bytes a partir de la clave fija utilizando SHA-256
    key = hashlib.sha256(KEY.encode()).digest()
    # Codificar la clave en base64 para asegurarnos de que sea url-safe
    key = base64.urlsafe_b64encode(key)
    return Fernet(key)

# Descifrar el texto utilizando la clave Fernet
def decrypt_text(encrypted_text, fernet):
    decrypted_text = fernet.decrypt(encrypted_text.encode()).decode()
    return decrypted_text

def connect():
    cnx = None
    while not cnx:
        try:
            cnx = sqlite3.connect(DATABASE_PATH)
            print("Connected to local database successfully!")
        except sqlite3.Error as e:
            print(f"Error connecting to local database: {e}")
            print("Reconnecting in 5 seconds please wait...")
            time.sleep(5)
    return cnx
