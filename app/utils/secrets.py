from hashlib import sha512
from secrets import token_hex


def create_token():
    return token_hex(64)


def hash_str(string: str) -> str:
    return sha512(string.encode("utf-8")).hexdigest()


def hash_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = token_hex(16)
    hashed_password = hash_str(salt + hash_str(password))
    return f"sha512${salt}${hashed_password}"


def verify_password(password: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split("$", 2)[1:]
    return hash_str(salt + hash_str(password)) == hashed
