from fastapi import Request, status, HTTPException
from fastapi.security import HTTPBearer

from jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com" and data["password"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales invalidas")