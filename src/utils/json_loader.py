from typing import List, Type, TypeVar
from pydantic import BaseModel, ValidationError
import json
from base.logger import get_logger
from firebase import bucket

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)

def load_json_templates(
    model: Type[T], 
    prefix: str
) -> List[T]:
    blobs = bucket.list_blobs(prefix=prefix)
    templates = []
    for blob in blobs:
        if blob.name.endswith(".json"):
            try:
                data = json.loads(blob.download_as_text())
                obj = model(**data)
                templates.append(obj)
            except ValidationError as e:
                logger.error(f"Error loading {blob.name}: {e}")
    return templates