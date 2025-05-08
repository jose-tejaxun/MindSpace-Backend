from cryptography.fernet import Fernet
import os

fernet = Fernet(os.getenv("FERNET_KEY"))

def encrypt(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
