
from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from auth import get_current_user, User  # Assuming auth is already implemented

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: PlainTextResponse(str(exc), status_code=429))
app.add_middleware(SlowAPIMiddleware)

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: int

@app.post("/predict", response_model=PredictionResponse)
@limiter.limit("5/minute")
async def predict(request: PredictionRequest, current_user: User = Depends(get_current_user)):
    # Your existing predict logic here
    return {"prediction": "Your prediction result"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
