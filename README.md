cat >> README.md << 'EOF'
# Inventory Management System

A Flask-based REST API with CRUD operations for managing retail inventory, enriched with product
data from the [OpenFoodFacts API](https://openfoodfacts.github.io/openfoodfacts-server/api/),
plus a CLI client for interacting with it.

## Features

- REST API: GET / POST / PATCH / DELETE on `/inventory`
- OpenFoodFacts lookup by barcode or product name
- CLI frontend for all operations
- Unit tests with pytest and unittest.mock

## Setup

```bash
git clone https://github.com/<your-username>/inventory-management-system.git
cd inventory-management-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the API

```bash
python run.py
```

Server runs at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/inventory` | List all inventory items |
| GET | `/inventory/<id>` | Get a single item by ID |
| POST | `/inventory` | Create a new item (`name`, `price`, `quantity` required) |
| PATCH | `/inventory/<id>` | Update one or more fields on an item |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/inventory/lookup?barcode=<code>` | Look up a product on OpenFoodFacts by barcode |
| GET | `/inventory/lookup?name=<text>` | Look up a product on OpenFoodFacts by name |

### Example: create an item

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "Almond Milk", "price": 4.99, "quantity": 25}'
```

## Running the CLI

With the API running in one terminal:

```bash
python cli/cli.py
```

Follow the on-screen menu to view, add, update, or delete items, or add an item straight from
an OpenFoodFacts lookup.

## Running Tests

```bash
pytest -v
```

## Notes on the OpenFoodFacts Integration

OpenFoodFacts rejects requests that don't send a descriptive `User-Agent` header (you'll get a
`403 Forbidden`, which the API wraps as a `502` from our own `/inventory/lookup` route since the
upstream call failed). `app/external_api.py` sends a `HEADERS` dict with every request:

```python
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (contact: your-email@example.com)"}
```

If you fork this project, swap in your own contact info in that string.

