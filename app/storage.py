"""
In-memory storage simulating a database using a Python list.
Each item is a dict with at least an 'id' key.
"""

inventory = []
_next_id = 1


def get_all_items():
    return inventory


def get_item_by_id(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


def add_item(data):
    global _next_id
    new_item = {
        "id": _next_id,
        "name": data.get("name"),
        "brand": data.get("brand", ""),
        "barcode": data.get("barcode", ""),
        "price": data.get("price", 0.0),
        "quantity": data.get("quantity", 0),
        "ingredients_text": data.get("ingredients_text", ""),
        "source": data.get("source", "manual"),
    }
    inventory.append(new_item)
    _next_id += 1
    return new_item


def update_item(item_id, data):
    item = get_item_by_id(item_id)
    if item is None:
        return None
    for key in ("name", "brand", "barcode", "price", "quantity", "ingredients_text", "source"):
        if key in data:
            item[key] = data[key]
    return item


def delete_item(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        return False
    inventory.remove(item)
    return True


def reset_storage():
    """Helper for tests — clears the list and resets the id counter."""
    global _next_id
    inventory.clear()
    _next_id = 1
