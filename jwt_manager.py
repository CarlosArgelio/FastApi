import os

from jwt import encode
from dotenv import load_dotenv

load_dotenv()

def create_token(data: dict):
    token: str = encode(payload=data, key=os.getenv("SECRET_KEY_TOKEN_JWT"), algorithm="HS256")
    return token