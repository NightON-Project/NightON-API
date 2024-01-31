import time
from typing import Dict
import jwt
from decouple import config

JWT_SECRET = 'no_tem_secret'# config('secret')
JWT_ALGORITHM = 'HS256'#config('algorithm')


#The secret key is used for encoding and decoding JWT strings.
# hash
# import os 
# import binascii
#binascii.hexlify(os.urandom(24))
#The algorithm value on the other hand is the type of algorithm used in the encoding process.


def tokenResponse(token: str):
    return {"access_token": token}

def signJWT(role_id: str) -> Dict[str, str]:
    """
    APPELER CA AVEC UN 
    """
    payload = {
        "role_id": role_id,
        "expires": time.time() + 60*1*1
    }
    token = jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return tokenResponse(token)


def decodeJWT(token: str) -> dict:
    """
    The decodeJWT function takes the token and decodes it with the aid of the jwt module 
    and then stores it in a decoded_token variable. Next, we returned decoded_token if 
    the expiry time is valid, otherwise, we returned None.
    A JWT is not encrypted. It's based64 encoded and signed. So anyone can decode the 
    token and use its data. But only the server can verify it's authenticity using 
    the JWT_SECRET.
    """

    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        print(f'Erreur_auth_handller() {e}')
        return {}