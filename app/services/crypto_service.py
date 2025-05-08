import os
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import sha256
from dotenv import load_dotenv

load_dotenv()

raw_key = os.getenv("ENCRYPTION_KEY")
key = sha256(raw_key.encode()).digest()
fernet = Fernet(urlsafe_b64encode(key))

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
