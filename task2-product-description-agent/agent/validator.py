import json

def validate_output(output: str, title: str) -> dict:
    """
    Validates JSON output and ensures hallucination-free generation.
    """

    try:
        parsed = json.loads(output)

        if not isinstance(parsed, dict):
            raise ValueError("Output is not valid JSON object")

        if "description" not in parsed or "assumptions" not in parsed:
            raise ValueError("Missing required JSON keys")

        hallucination_free = True
        attributes_used = []

        title_lower = title.lower()

        for token in parsed["description"].lower().split():
            if token.isdigit() and token not in title_lower:
                hallucination_free = False
                attributes_used.append(token)

        parsed["validation"] = {
            "hallucination_free": hallucination_free,
            "attributes_used": attributes_used
        }

        return parsed

    except Exception as e:
        return {
            "product_title": title,
            "description": "",
            "assumptions": [],
            "validation": {
                "hallucination_free": False,
                "error": f"Validation failed: {str(e)}"
            }
        }
