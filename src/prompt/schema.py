from base.schema import BaseMCPModel

class PromptSchema(BaseMCPModel):    
    content: str
    role: str = "user"
    