"""
menu_service.py - Food menu business logic, validation, and price calculations.

Fields:
- item_id: Unique identifier (e.g., ITEM101)
- item_name: Name of the food/beverage item
- category: Food category (e.g., Fast Food, Beverages, Snacks, Main Course)
- price: Price in INR (stored as Decimal string with 2 decimal places)

Rules:
- Item name cannot be empty.
- Price must be a valid number greater than zero.
- Decimal is used for accurate financial calculations.
"""

from decimal import Decimal, InvalidOperation
from . import csv_storage

FILENAME = 'menu.csv'
ID_FIELD = 'item_id'

# Standard sample categories
CATEGORIES = [
    'Fast Food',
    'Beverages',
    'Snacks',
    'Main Course',
    'Desserts',
]


def validate_menu_item(item_name: str, category: str, price: str | float | Decimal) -> tuple[bool, str, Decimal]:
    """
    Validate item name, category, and price.
    Returns (True, '', Decimal(price)) if valid, or (False, 'error', Decimal(0)) if invalid.
    """
    clean_name = item_name.strip() if item_name else ''
    clean_category = category.strip() if category else 'General'

    if not clean_name:
        return False, "Menu item name cannot be empty.", Decimal('0')
    if len(clean_name) < 2:
        return False, "Menu item name must be at least 2 characters long.", Decimal('0')

    try:
        price_dec = Decimal(str(price).strip())
        if price_dec <= Decimal('0'):
            return False, "Price must be strictly greater than ₹0.", Decimal('0')
        # Quantize to 2 decimal places for consistent storage
        price_dec = price_dec.quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError, TypeError):
        return False, "Invalid price format. Please enter a valid positive number (e.g. 100 or 99.50).", Decimal('0')

    return True, clean_category, price_dec


def get_all_menu_items(search_query: str = None, category_filter: str = None) -> list[dict]:
    """
    Retrieve all menu items, optionally filtered by name/category query.
    """
    items = csv_storage.read_all(FILENAME)

    if category_filter and category_filter != 'All':
        items = [i for i in items if i.get('category', '').lower() == category_filter.lower()]

    if search_query:
        query = search_query.strip().lower()
        items = [
            i for i in items
            if query in i.get('item_name', '').lower() or query in i.get('category', '').lower()
        ]

    return items


def get_menu_item_by_id(item_id: str) -> dict | None:
    """
    Fetch a menu item by its item_id.
    """
    return csv_storage.find_by_id(FILENAME, ID_FIELD, item_id)


def add_menu_item(item_name: str, category: str, price: str | float | Decimal) -> tuple[bool, str, dict | None]:
    """
    Validate and save a new menu item into menu.csv.
    Generates a unique item_id like ITEM101, ITEM102.
    """
    is_valid, category_clean, price_dec = validate_menu_item(item_name, category, price)
    if not is_valid:
        return False, category_clean, None

    clean_name = item_name.strip()

    # Prevent duplicate item names (case-insensitive)
    existing_items = get_all_menu_items()
    for item in existing_items:
        if item.get('item_name', '').strip().lower() == clean_name.lower():
            return False, f"A menu item with the name '{clean_name}' already exists.", None

    new_id = csv_storage.generate_new_id(FILENAME, ID_FIELD, prefix='ITEM', start_num=101)
    record = {
        'item_id': new_id,
        'item_name': clean_name,
        'category': category_clean,
        'price': f"{price_dec:.2f}",
    }
    csv_storage.append_record(FILENAME, record)
    return True, f"Menu item '{clean_name}' added successfully with ID {new_id}.", record


def update_menu_item(item_id: str, item_name: str, category: str, price: str | float | Decimal) -> tuple[bool, str]:
    """
    Validate and update an existing menu item.
    Note: Updating a menu item's price will not affect past orders,
    because past orders store historical unit prices inside order_items.csv.
    """
    is_valid, category_clean, price_dec = validate_menu_item(item_name, category, price)
    if not is_valid:
        return False, category_clean

    clean_name = item_name.strip()
    existing_item = get_menu_item_by_id(item_id)
    if not existing_item:
        return False, f"Menu item with ID {item_id} not found."

    # Check for name collision with other items
    all_items = get_all_menu_items()
    for item in all_items:
        if item.get('item_id') != item_id and item.get('item_name', '').strip().lower() == clean_name.lower():
            return False, f"Another item with name '{clean_name}' already exists."

    updated_data = {
        'item_name': clean_name,
        'category': category_clean,
        'price': f"{price_dec:.2f}",
    }
    success = csv_storage.update_record(FILENAME, ID_FIELD, item_id, updated_data)
    if success:
        return True, f"Menu item {item_id} ('{clean_name}') updated successfully."
    return False, "Failed to update menu item."


def delete_menu_item(item_id: str) -> tuple[bool, str]:
    """
    Delete a menu item from menu.csv.
    """
    item = get_menu_item_by_id(item_id)
    if not item:
        return False, f"Menu item with ID {item_id} not found."

    success = csv_storage.delete_record(FILENAME, ID_FIELD, item_id)
    if success:
        return True, f"Menu item {item_id} ('{item.get('item_name')}') deleted successfully."
    return False, "Failed to delete menu item."

