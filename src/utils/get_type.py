from typing import List, Dict, Any, Literal, Optional, Union

def get_type(type_str: str):
    """Convert string type annotations to actual type objects."""
    # Create a namespace with all the typing imports available
    type_namespace = {
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'List': List,
        'Dict': Dict,
        'Any': Any,
        'Literal': Literal,
        'Optional': Optional,
        'Union': Union,
        'bytes': bytes,
        # Add other types as needed
    }
    
    try:
        # Evaluate the type string in the proper namespace
        return eval(type_str, {"__builtins__": {}}, type_namespace)
    except Exception as e:
        print(f"Warning: Could not parse type '{type_str}': {e}")
        # Fallback to Any if we can't parse the type
        return Any