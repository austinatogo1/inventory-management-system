from unittest.mock import patch, MagicMock
from cli import cli


@patch("cli.cli.requests.get")
def test_view_all_items_empty(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    cli.view_all_items()
    captured = capsys.readouterr()
    assert "No items in inventory." in captured.out


@patch("cli.cli.requests.get")
def test_view_all_items_with_data(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "name": "Milk", "price": 3.5, "quantity": 5}
    ]
    mock_get.return_value = mock_response

    cli.view_all_items()
    captured = capsys.readouterr()
    assert "Milk" in captured.out


@patch("cli.cli.requests.post")
@patch("builtins.input", side_effect=["Bread", "2.5", "10"])
def test_add_item_manually(mock_input, mock_post, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "Bread", "price": 2.5, "quantity": 10}
    mock_post.return_value = mock_response

    cli.add_item_manually()
    captured = capsys.readouterr()
    assert "Item added" in captured.out
    assert mock_input.call_count == 3  # Should prompt for name, price, and quantity


@patch("builtins.input", side_effect=["Bread", "abc", "10"])
def test_add_item_manually_invalid_price(mock_input, capsys):
    cli.add_item_manually()
    captured = capsys.readouterr()
    assert "Price must be a number" in captured.out
    assert mock_input.call_count == 3  # Should prompt for price again
