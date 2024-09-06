
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi_limiter.depends import RateLimiter

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes token expiration

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={"admin": "Admin access", "user": "User access"})

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a new JWT access token with an optional expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """
    Creates a new refresh token for prolonged sessions (7 days expiration).
    """
    return create_access_token(data, expires_delta=timedelta(days=7))

def get_current_user_with_scope(token: str = Depends(oauth2_scheme), scope: str = "user"):
    """
    Validates the OAuth2 token and ensures the required scope is present.
    """
    user = validate_token(token)  # Assuming validate_token is implemented elsewhere
    token_scopes = ["user"]  # Example: fetched from token or decoded claims
    if scope not in token_scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

@app.get("/secure-endpoint", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def secure_endpoint():
    """
    Example endpoint with rate limiting (5 requests per minute).
    """
    return {"message": "This endpoint is rate limited to 5 requests per minute."}

@app.get("/admin-endpoint", dependencies=[Depends(get_current_user_with_scope(scope="admin"))])
async def admin_endpoint():
    """
    Admin-only endpoint using OAuth2 scope validation.
    """
    return {"message": "You have admin access."}
