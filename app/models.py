"""
Lightweight validation for inventory payloads.
"""

REQUIRED_FIELDS = ["name", "price", "quantity"]


def validate_item_payload(data):
    errors = []
    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, ""):
            errors.append(f"'{field}' is required.")

    if "price" in data and data["price"] is not None:
        try:
            float(data["price"])
        except (ValueError, TypeError):
            errors.append("'price' must be a number.")

    if "quantity" in data and data["quantity"] is not None:
        try:
            int(data["quantity"])
        except (ValueError, TypeError):
            errors.append("'quantity' must be an integer.")

    return errors
