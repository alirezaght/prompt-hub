from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from static.oauth_authorization import oauth_authorization_server
from static.oauth_protected import oauth_protected_resource
from middleware.cloudflare import cloudflare_middleware
from middleware.oauth import oath_middleware
from prompt.actions.register_prompts import register_prompts
from middleware.context import RequestContextMiddleware

from base.logger import get_logger

logger = get_logger(__name__)


mcp = FastMCP("Prompt Hub")

 
app = mcp.streamable_http_app()

app.add_route(
    "/.well-known/oauth-authorization-server",
    oauth_authorization_server,
)
app.add_route(
    "/.well-known/oauth-protected-resource",
    oauth_protected_resource,
)

register_prompts(mcp)

cloudflare_middleware(app)

oath_middleware(app, "/mcp")

app.add_middleware(
    RequestContextMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


