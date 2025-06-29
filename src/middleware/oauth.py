from base.logger import get_logger
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.base.schema import UserInfo

logger = get_logger(__name__)

def verifier(token: str):
    try:
        import httpx
        logger.info(f"Raw token: {token}")        
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get("https://prompt-hub.eu.auth0.com/userinfo", headers=headers)
        decoded = response.json()
        client_id = decoded.get(f"https://prompt-hub.ai/client_id")
        if not client_id:
            logger.error("Client ID not found in token payload")
            raise HTTPException("Client ID not found in token payload")
        data = {**decoded, **{"client_id": client_id}}
        return UserInfo(**data) 
    except Exception as e:
        logger.error(f"HTTP error while verifying token: {e}")
        raise HTTPException(f"HTTP error while verifying token: {e}")

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
            
            logger.info(f"Authenticated user: {user.sub} with client_id: {user.client_id}")
            request.state.user = user
            logger.info(f"Request state user: {request.state.user}")
        
        response = await call_next(request)        
        logger.info(f"Response status code: {response.status_code}")

        return response