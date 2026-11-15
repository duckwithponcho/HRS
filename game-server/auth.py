#NOTE: Put JWT verification logic here

import jwt

PUBLIC_KEY_PATH = "keys/public.pem"

with open(PUBLIC_KEY_PATH, "r") as key_file:
    PUBLIC_KEY = key_file.read()
    
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, 
                             algorithms=["RS256"],
                             options={"require": ["exp","sub"]})
        return payload
    except jwt.InvalidTokenError:
        return None