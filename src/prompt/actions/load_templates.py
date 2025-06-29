from ..schema import PromptSchema
from typing import Dict
from firebase import bucket
import json
from base.logger import get_logger
from pydantic import ValidationError

logger = get_logger(__name__)

def load_json_templates(prefix="prompts/") -> Dict[str, PromptSchema]:
    blobs = bucket.list_blobs(prefix=prefix)
    templates = {}
    for blob in blobs:
        if blob.name.endswith(".json"):
            try:
                data = json.loads(blob.download_as_text())
                prompt = PromptSchema(**data)
                templates[prompt.prompt_name] = prompt
                logger.info(f"Loaded prompt: {prompt.prompt_name}")
            except ValidationError as e:
                logger.error(f"Error loading {blob.name}: {e}")
    return templates