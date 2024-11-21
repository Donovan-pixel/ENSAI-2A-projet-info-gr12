import hashlib


def hash_password(password, sel=""):
    """Hachage du mot de passe"""
    if salt is None:
        salt = os.urandom(16).hex()
    password_bytes = password.encode("utf-8") + sel.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()
