from pydantic import BaseModel

class UserInfo(BaseModel):
    client_id: str
    sub: str
    email: str
    email_verified: bool
    model_config = {
        "extra": "allow",        
    }
    
class BaseMCPModel(BaseModel):    
    name: str = ""
    title: str = ""
    description: str = ""
    args: list[dict] = []
    