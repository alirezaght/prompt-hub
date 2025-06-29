from fastapi.responses import JSONResponse


async def oauth_authorization_server(request):
    # Example: fetch from Auth0, modify, then return
    data = {
        "issuer": "https://prompt-hub.eu.auth0.com/",
        "authorization_endpoint": "https://prompt-hub.eu.auth0.com/authorize?scope=openid%20email%20offline_access%20email_verified",
        "token_endpoint": "https://prompt-hub.eu.auth0.com/oauth/token", 
        "response_types_supported":["code"],
        "registration_endpoint":"https://prompt-hub.eu.auth0.com/oidc/register",
        "code_challenge_methods_supported":
        [
            "S256",
            "plain"
        ],
           
    }
    return JSONResponse(data)