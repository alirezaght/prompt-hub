from base.schema import BaseMCPModel
from typing import Optional

class ToolSchema(BaseMCPModel):    
    uri: str
    structured_output: Optional[bool] = None
    
    