from ..schema import PromptSchema
from mcp.server.fastmcp.prompts.base import Message
import inspect
from mcp.server.fastmcp import FastMCP
from .load_templates import load_json_templates
from mcp.server.fastmcp.prompts.base import Prompt


def make_prompt_fn(prompt: PromptSchema):
    args = prompt.prompt_args
    arg_names = [a["name"] for a in args]

    def prompt_func_factory(_template, _role, _arg_names):
        async def f(**kwargs):
            text = _template
            for k, v in kwargs.items():
                text = text.replace(f"{{{k}}}", str(v))
            return [Message(role=_role, content=text)]
        # Properly annotate the function
        f.__annotations__ = {a['name']: str for a in args}
        return f

    params = [
        inspect.Parameter(arg["name"], inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=arg["type"])
        for arg in args
    ]
    async_fn = prompt_func_factory(prompt.content, prompt.role, arg_names)
    async_fn.__signature__ = inspect.Signature(params)
    async_fn.__name__ = prompt.prompt_name

    return async_fn

def register_prompts(mcp: FastMCP):    
    for prompt_name, prompt in load_json_templates().items():
        async_fn = make_prompt_fn(prompt)
        final_prompt = Prompt.from_function(async_fn, name=prompt_name, title=prompt.prompt_title, description=prompt.prompt_desc)
        mcp.add_prompt(final_prompt)