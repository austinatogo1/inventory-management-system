from flask import Blueprint, request, jsonify
from app import storage
from app.models import validate_item_payload
from app.external_api import search_openfoodfacts

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/inventory", methods=["GET"])
def list_items():
    return jsonify(storage.get_all_items()), 200


@inventory_bp.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = storage.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json(silent=True) or {}
    errors = validate_item_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_item = storage.add_item(data)
    return jsonify(new_item), 201


@inventory_bp.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_item(item_id):
    data = request.get_json(silent=True) or {}
    updated = storage.update_item(item_id, data)
    if updated is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated), 200


@inventory_bp.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    deleted = storage.delete_item(item_id)
    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": f"Item {item_id} deleted"}), 200


@inventory_bp.route("/inventory/lookup", methods=["GET"])
def lookup_item():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "Provide a 'barcode' or 'name' query param"}), 400

    result, error = search_openfoodfacts(barcode=barcode, name=name)
    if error:
        return jsonify({"error": error}), 502
    if result is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(result), 200
