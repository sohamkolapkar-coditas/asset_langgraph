import re
import json


def _sanitize_json_strings(text: str) -> str:
    """Replace literal control characters inside JSON string values with their escape sequences.

    The LLM occasionally emits real newlines/tabs inside string values, which is invalid JSON.
    This walks through the text character-by-character, tracking whether we are inside a
    JSON string, and replaces bare control characters with their \n / \t / \r equivalents.
    """
    result = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            result.append(ch)
            escape_next = False
            continue
        if ch == "\\" and in_string:
            result.append(ch)
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            result.append(ch)
            continue
        if in_string and ch in ("\n", "\r", "\t"):
            # Replace bare control character with its JSON escape sequence
            result.append({"\\n": "\\n", "\n": "\\n", "\r": "\\r", "\t": "\\t"}.get(ch, "\\n"))
            continue
        result.append(ch)
    return "".join(result)


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
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        # Fallback: sanitize bare control characters inside string values and retry
        return json.loads(_sanitize_json_strings(stripped))
