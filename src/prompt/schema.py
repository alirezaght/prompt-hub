from pydantic import BaseModel

class PromptSchema(BaseModel):
    prompt_name: str
    prompt_title: str
    prompt_desc: str = ""
    prompt_args: list[dict] = []
    content: str
    role: str = "user"
    