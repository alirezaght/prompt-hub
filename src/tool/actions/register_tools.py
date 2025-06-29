from ..schema import ToolSchema
import inspect
from mcp.server.fastmcp import FastMCP
from utils.json_loader import load_json_templates
from middleware.context import get_current_request
from utils.get_type import get_type

def make_tool_fn(resource: ToolSchema):
    args = resource.args

    def tool_func_factory(uri):
        async def f(**kwargs):
            import requests
            user = get_current_request().state.user
            json = {**kwargs, **user.dict()} if user else kwargs
            response = requests.post(uri, json=json)
            return response.text
        # Properly annotate the function
        f.__annotations__ = {a['name']: get_type(a['type']) for a in args}
        return f

    params = [
        inspect.Parameter(arg["name"], inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=get_type(arg["type"]))
        for arg in args
    ]
    async_fn = tool_func_factory(resource.uri)
    async_fn.__signature__ = inspect.Signature(params)
    async_fn.__name__ = resource.name

    return async_fn

def register_tools(mcp: FastMCP):    
    for tool in load_json_templates(ToolSchema, "tools/"):
        async_fn = make_tool_fn(tool)        
        mcp.add_tool(async_fn,
                     name=tool.name,
                     title=tool.title,
                     description=tool.description,
                     structured_output=tool.structured_output,)