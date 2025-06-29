from base.logger import get_logger
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.base.schema import UserInfo
from base.cache import get_from_cache, put_to_cache

logger = get_logger(__name__)

def verifier(token: str):
    try:
        cache = get_from_cache(token)
        if cache:
            return UserInfo(**cache)
        import httpx
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get("https://prompt-hub.eu.auth0.com/userinfo", headers=headers)
        decoded = response.json()
        client_id = decoded.get(f"https://prompt-hub.ai/client_id")
        if not client_id:
            logger.error("Client ID not found in token payload")
            raise ValueError("Client ID not found in token payload")
        data = {**decoded, **{"client_id": client_id}}
        put_to_cache(token, data, expiration=3600)  # Cache for 1 hour
        return UserInfo(**data) 
    except Exception as e:
        logger.error(f"HTTP error while verifying token: {e}")
        raise ValueError(f"HTTP error while verifying token: {e}")

def oath_middleware(app, path_prefix="/mcp"):    
    @app.middleware("http")
    async def oauth_check(request: Request, call_next):
        # Code before passing to the next handler (e.g. logging, modify request)
        print(f"Request: {request.method} {request.url}")
        if request.url.path.startswith(path_prefix):        
            token = request.headers.get("Authorization").split(" ")[-1] if request.headers.get("Authorization") else None
            if not token:
                return JSONResponse({"error": "Authorization header missing"}, status_code=401)
            
            user = verifier(token)
            if not user:
                return JSONResponse({"error": "Invalid token"}, status_code=401)
            
            request.state.user = user
        
        response = await call_next(request)        

        return response