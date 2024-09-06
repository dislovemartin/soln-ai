from jose import JWTError, jwt

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"

def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError()
        return user_id
    except JWTError:
        return None