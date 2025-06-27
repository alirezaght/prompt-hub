from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message
import firebase_admin
from firebase_admin import credentials, storage
import uvicorn
import json
import inspect
from pydantic import ValidationError
from schema import PromptSchema
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# -- Firebase Setup --
cred = credentials.Certificate("firebase-service-account.json")
firebase_admin.initialize_app(cred, {    
    "storageBucket": "prompt-hub-2bdbf.firebasestorage.app"
})
bucket = storage.bucket()

# -- MCP Setup --
mcp = FastMCP("Prompt Hub")

def load_json_templates_from_firebase(prefix="prompts/") -> Dict[str, PromptSchema]:
    blobs = bucket.list_blobs(prefix=prefix)
    templates = {}
    for blob in blobs:
        if blob.name.endswith(".json"):
            try:
                data = json.loads(blob.download_as_text())
                prompt = PromptSchema(**data)
                templates[prompt.prompt_name] = prompt
            except ValidationError as e:
                logger.error(f"Error loading {blob.name}: {e}")
    return templates

def make_prompt_fn(prompt: PromptSchema):
    args = prompt.prompt_args
    arg_names = [a["name"] for a in args]

    def prompt_func_factory(_template, _role, _arg_names):
        async def f(**kwargs):
            text = _template
            for k, v in kwargs.items():
                text = text.replace(f"{{{k}}}", str(v))
            return [Message(role=_role, content=text)]
        return f

    params = [
        inspect.Parameter(arg["name"], inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
        for arg in args
    ]
    async_fn = prompt_func_factory(prompt.content, prompt.role, arg_names)
    async_fn.__signature__ = inspect.Signature(params)
    async_fn.__name__ = prompt.prompt_name

    return async_fn

# Register dynamic prompts
for prompt_name, prompt in load_json_templates_from_firebase().items():
    async_fn = make_prompt_fn(prompt)
    mcp.prompt(
        name=prompt.prompt_name,
        description=prompt.prompt_desc
    )(async_fn)

if __name__ == "__main__":
    uvicorn.run(mcp.streamable_http_app(), host="localhost", port=8080)