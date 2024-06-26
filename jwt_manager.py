import os

from jwt import encode, decode
from dotenv import load_dotenv

load_dotenv()

def create_token(data: dict):
    token: str = encode(payload=data, key=os.getenv("SECRET_KEY_TOKEN_JWT"), algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=os.getenv("SECRET_KEY_TOKEN_JWT"), algorithms=['HS256'])
    return data