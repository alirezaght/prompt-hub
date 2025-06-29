import requests
import ipaddress
from fastapi import Request, HTTPException
from base.logger import get_logger

logger = get_logger(__name__)



# Download Cloudflare's IPs once at startup
CLOUDFLARE_IPS_V4 = requests.get("https://www.cloudflare.com/ips-v4").text.splitlines()
CLOUDFLARE_IPS_V6 = requests.get("https://www.cloudflare.com/ips-v6").text.splitlines()

def is_cloudflare_ip(ip: str) -> bool:
    ip_obj = ipaddress.ip_address(ip)
    for cidr in CLOUDFLARE_IPS_V4 + CLOUDFLARE_IPS_V6:
        if ip_obj in ipaddress.ip_network(cidr):
            return True
    return False

def cloudflare_middleware(app):
    @app.middleware("http")
    async def only_allow_cloudflare(request: Request, call_next):    
        if request.url.hostname == "localhost":            
            return await call_next(request)
        client_ip = (
            request.headers.get("fly-client-ip")
            or request.headers.get("Fly-Client-IP")
            or request.client.host
        )
        client_ip = client_ip.split(",")[0].strip()
        logger.info(f"Client IP: {client_ip}")
        if not is_cloudflare_ip(client_ip):
            logger.error(f"Access denied for IP: {client_ip}")
            raise HTTPException(status_code=403, detail="Access denied: Only requests from Cloudflare are allowed.")
        return await call_next(request)
    
