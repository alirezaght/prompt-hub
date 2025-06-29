from ..schema import PromptSchema
from mcp.server.fastmcp.prompts.base import Message
import inspect
from mcp.server.fastmcp import FastMCP
from utils.json_loader import load_json_templates
from mcp.server.fastmcp.prompts.base import Prompt
from fastapi import UploadFile


def make_prompt_fn(prompt: PromptSchema):
    args = prompt.args

    def prompt_func_factory(_template, _role):
        async def f(**kwargs):
            text = _template
            for k, v in kwargs.items():
                text = text.replace(f"{{{k}}}", str(v))
            return [Message(role=_role, content=text)]
        # Properly annotate the function
        f.__annotations__ = {a['name']: a['type'] for a in args}
        return f

    params = [
        inspect.Parameter(arg["name"], inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=arg["type"])
        for arg in args
    ]
    async_fn = prompt_func_factory(prompt.content, prompt.role)
    async_fn.__signature__ = inspect.Signature(params)
    async_fn.__name__ = prompt.name

    return async_fn

def register_prompts(mcp: FastMCP):    
    for prompt in load_json_templates(PromptSchema, "prompts/"):
        async_fn = make_prompt_fn(prompt)
        final_prompt = Prompt.from_function(async_fn, name=prompt.title, title=prompt.title, description=prompt.description)
        mcp.add_prompt(final_prompt)