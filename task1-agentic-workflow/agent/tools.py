import re
from typing import Dict


# ==============================
# DOMAIN CONSTANTS
# ==============================

PRODUCT_TAXONOMY = {
    "Electronics": {
        "Smartphone": ["phone", "smartphone", "mobile", "galaxy", "iphone"],
        "Laptop": ["laptop", "macbook", "notebook"],
        "TV": ["tv", "oled", "led"]
    },
    "Clothing": {
        "Topwear": ["shirt", "t-shirt"],
        "Bottomwear": ["jeans", "trousers"]
    }
}

BRANDS = ["samsung", "apple", "oneplus", "xiaomi", "sony"]
COLORS = ["black", "white", "blue", "green", "red"]


# ==============================
# INTERNAL VALIDATION
# ==============================

def _validate_title(title: str) -> str:
    """
    Validates product title input.
    """
    if not isinstance(title, str):
        raise TypeError("Product title must be a string")

    title = title.strip()
    if not title:
        raise ValueError("Product title cannot be empty")

    return title


# ==============================
# CLASSIFICATION TOOL
# ==============================

def classify_product(title: str) -> Dict:
    """
    Classifies a product into category and sub-category with confidence.
    """
    try:
        title = _validate_title(title)
        title_lower = title.lower()

        signals = []

        for category, subcats in PRODUCT_TAXONOMY.items():
            for subcat, keywords in subcats.items():
                for kw in keywords:
                    if kw in title_lower:
                        signals.append(kw)
                        confidence = min(0.7 + (0.05 * len(signals)), 0.95)
                        return {
                            "category": category,
                            "sub_category": subcat,
                            "confidence": round(confidence, 2),
                            "signals": list(set(signals))
                        }

        return {
            "category": "Unknown",
            "sub_category": "Unknown",
            "confidence": 0.3,
            "signals": []
        }

    except Exception as e:
        return {
            "error": f"Classification failed: {str(e)}"
        }


# ==============================
# ATTRIBUTE EXTRACTION TOOL
# ==============================

def extract_product_attributes(title: str) -> Dict:
    """
    Extracts structured product attributes using regex and heuristics.
    """
    try:
        title = _validate_title(title)
        title_lower = title.lower()
        attributes = {}

        # Brand detection
        for brand in BRANDS:
            if brand in title_lower:
                attributes["brand"] = brand.capitalize()
                break

        # Memory (GB / TB)
        memory_match = re.search(r'(\d+)\s?(gb|tb)', title_lower)
        if memory_match:
            value = int(memory_match.group(1))
            unit = memory_match.group(2)
            attributes["memory_gb"] = value * 1024 if unit == "tb" else value

        # Screen size
        screen_match = re.search(r'(\d+(\.\d+)?)\s?inch', title_lower)
        if screen_match:
            attributes["screen_size_inch"] = float(screen_match.group(1))

        # Color
        for color in COLORS:
            if color in title_lower:
                attributes["color"] = color.capitalize()
                break

        # Model detection (heuristic)
        model_match = re.search(r'(galaxy\s?s\d+|iphone\s?\d+)', title_lower)
        if model_match:
            attributes["model"] = model_match.group(1).title()

        if not attributes:
            raise ValueError("No extractable attributes found")

        return attributes

    except Exception as e:
        return {
            "error": f"Attribute extraction failed: {str(e)}"
        }


# ==============================
# SUMMARIZATION TOOL
# ==============================

def summarize_product(title: str) -> str:
    """
    Summarizes a product title safely.
    """
    try:
        title = _validate_title(title)

        if len(title.split()) < 6:
            return title  # No summarization needed

        return f"Concise product summary: {title}"

    except Exception as e:
        return f"Summarization failed: {str(e)}"
