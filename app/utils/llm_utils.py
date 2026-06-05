import re
import json


def parse_llm_json(raw: str) -> dict:
    """Strip optional markdown code fences then parse JSON.

    Raises ValueError if the content is empty, json.JSONDecodeError if malformed.
    """
    if not isinstance(raw, str):
        raw = ""
    stripped = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    stripped = re.sub(r"\s*```$", "", stripped.strip()).strip()
    if not stripped:
        raise ValueError("LLM returned an empty response")
    return json.loads(stripped)
