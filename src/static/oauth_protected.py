from fastapi.responses import JSONResponse

async def oauth_protected_resource(request):
    # Return required keys for MCP/OAuth spec
    return JSONResponse({
        "resource": "https://prompt-hub.ai",
        "authorization_servers": ["https://prompt-hub.ai"],
        "scopes_supported": ["openid", "profile", "email"],
        "bearer_methods_supported": ["header"]
    })