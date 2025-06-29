from base.schema import BaseMCPModel

class ResourceSchema(BaseMCPModel):    
    uri: str
    mime_type: str
    
    