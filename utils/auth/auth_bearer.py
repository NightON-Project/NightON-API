from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT, generateJWT
import bcrypt
import jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pw


def check_password(plain_password, hashed_password):
    if isinstance(plain_password, str):
        plain_password = plain_password.encode("utf-8")
    byte_hashed_password = bytes(hashed_password)
    return bcrypt.checkpw(plain_password, byte_hashed_password)


def token_required(f):
    def wrapper(*args, **kargs):
        token_with_bearer = Request.headers.get("Authorization")
        if not token_with_bearer:
            raise HTTPException(status_code=401, detail="Token is missing")
        _, token = token_with_bearer.split(" ", 1)
        try:
            data = decodeJWT(token)
            current_role = data["role_id"]
        except Exception as e:
            print(f"Erreur_token-required :: {e}")
            raise HTTPException(status_code=401, detail="Unauthorized")
        return f(current_role, *args, **kargs)

    return wrapper
