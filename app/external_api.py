"""
Integration with the OpenFoodFacts API.
Docs: https://openfoodfacts.github.io/openfoodfacts-server/api/
"""

import requests

BASE_URL = "https://world.openfoodfacts.org"
TIMEOUT = 8  # seconds
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (contact: your-email@example.com)"}


def _format_product(raw_product, source_barcode=None):
    """Normalize an OpenFoodFacts product payload into our inventory shape."""
    return {
        "name": raw_product.get("product_name") or "Unknown product",
        "brand": raw_product.get("brands", ""),
        "barcode": source_barcode or raw_product.get("code", ""),
        "ingredients_text": raw_product.get("ingredients_text", ""),
        "source": "openfoodfacts",
    }


def search_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return None, f"Failed to reach OpenFoodFacts: {e}"

    data = response.json()
    if data.get("status") != 1:
        return None, None  # not found, no error

    return _format_product(data["product"], source_barcode=barcode), None


def search_by_name(name):
    url = f"{BASE_URL}/cgi/search.pl"
    params = {"search_terms": name, "json": 1, "page_size": 1}
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return None, f"Failed to reach OpenFoodFacts: {e}"

    data = response.json()
    products = data.get("products", [])
    if not products:
        return None, None

    return _format_product(products[0]), None


def search_openfoodfacts(barcode=None, name=None):
    """
    Unified lookup used by the Flask route and the CLI.
    Returns (result_dict_or_None, error_message_or_None).
    """
    if barcode:
        return search_by_barcode(barcode)
    if name:
        return search_by_name(name)
    return None, "No barcode or name provided"
