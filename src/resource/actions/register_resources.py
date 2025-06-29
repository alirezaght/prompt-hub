from ..schema import ResourceSchema
from mcp.server.fastmcp.prompts.base import Message
import inspect
from mcp.server.fastmcp import FastMCP
from utils.json_loader import load_json_templates
from mcp.server.fastmcp.resources import FunctionResource
from utils.get_type import get_type


def make_resource_fn(resource: ResourceSchema):
    args = resource.args

    def resource_func_factory(uri):
        async def f(**kwargs):
            import requests
            response = requests.get(uri, params=kwargs)
            return response.text
        # Properly annotate the function
        f.__annotations__ = {a['name']: get_type(a['type']) for a in args}
        return f

    params = [
        inspect.Parameter(arg["name"], inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=get_type(arg["type"]))
        for arg in args
    ]
    async_fn = resource_func_factory(resource.uri)
    async_fn.__signature__ = inspect.Signature(params)
    async_fn.__name__ = resource.name

    return async_fn

def register_resources(mcp: FastMCP):    
    for resource in load_json_templates(ResourceSchema, "resources/"):
        async_fn = make_resource_fn(resource)
        final_resource = FunctionResource.from_function(
            async_fn,
            uri=resource.uri,
            name=resource.name,
            title=resource.title,
            description=resource.description,
            mime_type=resource.mime_type
        )
        mcp.add_resource(final_resource)