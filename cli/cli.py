"""
CLI client for the Inventory Management API.
Run the Flask server first (python run.py), then run this file.
"""

import requests

API_BASE = "http://127.0.0.1:5000"


def view_all_items():
    resp = requests.get(f"{API_BASE}/inventory")
    items = resp.json()
    if not items:
        print("No items in inventory.")
        return
    for item in items:
        print(f"[{item['id']}] {item['name']} — ${item['price']} — qty: {item['quantity']}")


def view_one_item():
    item_id = input("Item ID: ").strip()
    resp = requests.get(f"{API_BASE}/inventory/{item_id}")
    if resp.status_code == 404:
        print("Item not found.")
        return
    print(resp.json())


def add_item_manually():
    name = input("Name: ").strip()
    price = input("Price: ").strip()
    quantity = input("Quantity: ").strip()

    try:
        payload = {"name": name, "price": float(price), "quantity": int(quantity)}
    except ValueError:
        print("Price must be a number and quantity must be an integer.")
        return

    resp = requests.post(f"{API_BASE}/inventory", json=payload)
    if resp.status_code == 201:
        print("Item added:", resp.json())
    else:
        print("Failed to add item:", resp.json())


def add_item_from_lookup():
    choice = input("Search by (b)arcode or (n)ame? ").strip().lower()
    params = {}
    if choice == "b":
        params["barcode"] = input("Barcode: ").strip()
    elif choice == "n":
        params["name"] = input("Product name: ").strip()
    else:
        print("Invalid choice.")
        return

    resp = requests.get(f"{API_BASE}/inventory/lookup", params=params)
    if resp.status_code != 200:
        print("Lookup failed:", resp.json().get("error", "unknown error"))
        return

    product = resp.json()
    print("Found:", product)

    price = input("Set retail price: ").strip()
    quantity = input("Set stock quantity: ").strip()
    try:
        product["price"] = float(price)
        product["quantity"] = int(quantity)
    except ValueError:
        print("Price must be a number and quantity must be an integer.")
        return

    resp = requests.post(f"{API_BASE}/inventory", json=product)
    if resp.status_code == 201:
        print("Item added:", resp.json())
    else:
        print("Failed to add item:", resp.json())


def update_item():
    item_id = input("Item ID to update: ").strip()
    field = input("Field to update (price/quantity): ").strip().lower()
    if field not in ("price", "quantity"):
        print("Only price or quantity can be updated here.")
        return

    value = input(f"New {field}: ").strip()
    try:
        value = float(value) if field == "price" else int(value)
    except ValueError:
        print("Invalid value type.")
        return

    resp = requests.patch(f"{API_BASE}/inventory/{item_id}", json={field: value})
    if resp.status_code == 200:
        print("Updated:", resp.json())
    else:
        print("Update failed:", resp.json())


def delete_item():
    item_id = input("Item ID to delete: ").strip()
    resp = requests.delete(f"{API_BASE}/inventory/{item_id}")
    if resp.status_code == 200:
        print(resp.json()["message"])
    else:
        print("Delete failed:", resp.json())


MENU = """
==== Inventory Management CLI ====
1. View all items
2. View one item
3. Add item manually
4. Add item via OpenFoodFacts lookup
5. Update item price/quantity
6. Delete item
0. Exit
"""


def main():
    actions = {
        "1": view_all_items,
        "2": view_one_item,
        "3": add_item_manually,
        "4": add_item_from_lookup,
        "5": update_item,
        "6": delete_item,
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option.")
            continue
        try:
            action()
        except requests.exceptions.ConnectionError:
            print("Could not reach the API. Is the Flask server running?")


if __name__ == "__main__":
    main()
