import hashlib
import os
from dotenv import load_dotenv


def hash_password(password, sel=""):
    """Hachage du mot de passe"""
    if sel is None:
        sel = os.urandom(16).hex()
    password_bytes = password.encode("utf-8") + sel.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


load_dotenv()
admin_password = os.getenv("ADMIN_PASSWORD")