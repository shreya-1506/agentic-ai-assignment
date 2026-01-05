def decide_generation_strategy(title: str, supplier_text: str | None) -> dict:
    """
    Explicit decision logic to determine generation strategy.
    """

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Product title must be a non-empty string")

    signals = []

    title_lower = title.lower()

    if any(x in title_lower for x in ["gb", "tb", "inch", "cm", "mah"]):
        signals.append("specifications_present")

    if supplier_text and len(supplier_text.strip()) > 30:
        signals.append("supplier_text_present")

    if len(signals) >= 2:
        strategy = "STRICT_GENERATION"
    elif len(signals) == 1:
        strategy = "SAFE_GENERATION_WITH_ASSUMPTIONS"
    else:
        strategy = "MINIMAL_DESCRIPTION"

    return {
        "strategy": strategy,
        "signals": signals
    }
