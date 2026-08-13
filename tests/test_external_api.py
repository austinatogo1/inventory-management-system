from unittest.mock import patch, MagicMock
from app.external_api import search_by_barcode, search_by_name, search_openfoodfacts


@patch("app.external_api.requests.get")
def test_search_by_barcode_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Water, almonds",
        },
    }
    mock_get.return_value = mock_response

    result, error = search_by_barcode("123456")
    assert error is None
    assert result["name"] == "Almond Milk"
    assert result["brand"] == "Silk"
    assert result["barcode"] == "123456"


@patch("app.external_api.requests.get")
def test_search_by_barcode_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 0}
    mock_get.return_value = mock_response

    result, error = search_by_barcode("000000")
    assert result is None
    assert error is None


@patch("app.external_api.requests.get")
def test_search_by_barcode_network_error(mock_get):
    import requests
    mock_get.side_effect = requests.exceptions.ConnectionError("no network")

    result, error = search_by_barcode("123456")
    assert result is None
    assert "Failed to reach OpenFoodFacts" in error


@patch("app.external_api.requests.get")
def test_search_by_name_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [
            {"product_name": "Oat Milk", "brands": "Oatly", "ingredients_text": "Oats, water"}
        ]
    }
    mock_get.return_value = mock_response

    result, error = search_by_name("oat milk")
    assert error is None
    assert result["name"] == "Oat Milk"


def test_search_openfoodfacts_no_params():
    result, error = search_openfoodfacts()
    assert result is None
    assert error == "No barcode or name provided"
