"""
order_service.py - Order placement, item snapshots, status updates, and reporting.

Orders CSV:
- order_id: Unique order identifier (e.g., ORD1001)
- customer_id: Reference to customer in customers.csv
- order_date: Timestamp of order placement (YYYY-MM-DD HH:MM)
- total_amount: Final calculated order sum (Decimal with 2 decimal places)
- status: Current order status (Pending, Preparing, Ready, Completed, Cancelled)

Order Items CSV:
- order_item_id: Unique order item ID (e.g., OI1001)
- order_id: Reference to orders.csv
- item_id: Reference to menu.csv
- item_name: Snapshot of food item name at time of order
- quantity: Number of portions ordered
- unit_price: Snapshot of unit price at time of order
- subtotal: quantity * unit_price

Important Rules:
- Unit prices and item names are permanently frozen in order_items.csv so future menu price changes never modify historical orders or bills.
- Cancelled orders are excluded from total sales calculations.
"""

from decimal import Decimal
from datetime import datetime
from . import csv_storage
from . import customer_service
from . import menu_service

ORDERS_FILE = 'orders.csv'
ORDER_ITEMS_FILE = 'order_items.csv'

VALID_STATUSES = ['Pending', 'Preparing', 'Ready', 'Completed', 'Cancelled']


def place_order(customer_id: str, raw_items: list[dict]) -> tuple[bool, str, dict | None]:
    """
    Place a new multi-item order.
    raw_items is a list of dicts with 'item_id' and 'quantity'.

    Steps:
    1. Validate customer exists.
    2. Validate that at least one valid item with quantity > 0 is selected.
    3. Look up each item in menu.csv to snapshot current name and price.
    4. Calculate item-wise subtotal and overall total using Decimal.
    5. Save order in orders.csv.
    6. Save items in order_items.csv.
    """
    # 1. Customer check
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer:
        return False, f"Selected customer (ID: {customer_id}) was not found.", None

    # 2. Consolidate and validate items
    item_quantities: dict[str, int] = {}
    for entry in raw_items:
        item_id = str(entry.get('item_id', '')).strip()
        qty_raw = entry.get('quantity', 0)
        if not item_id:
            continue
        try:
            qty = int(qty_raw)
            if qty > 0:
                item_quantities[item_id] = item_quantities.get(item_id, 0) + qty
        except (ValueError, TypeError):
            continue

    if not item_quantities:
        return False, "Order must contain at least one valid menu item with a quantity of 1 or more.", None

    # 3. Snapshot items and calculate subtotals
    order_items_to_save = []
    total_amount = Decimal('0.00')

    for item_id, quantity in item_quantities.items():
        menu_item = menu_service.get_menu_item_by_id(item_id)
        if not menu_item:
            return False, f"Menu item ID '{item_id}' does not exist.", None

        item_name = menu_item.get('item_name')
        unit_price = Decimal(menu_item.get('price', '0.00'))
        subtotal = (unit_price * quantity).quantize(Decimal('0.01'))
        total_amount += subtotal

        order_items_to_save.append({
            'item_id': item_id,
            'item_name': item_name,
            'quantity': quantity,
            'unit_price': f"{unit_price:.2f}",
            'subtotal': f"{subtotal:.2f}",
        })

    # 4. Generate Order ID and record
    order_id = csv_storage.generate_new_id(ORDERS_FILE, 'order_id', prefix='ORD', start_num=1001)
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M')

    order_record = {
        'order_id': order_id,
        'customer_id': customer_id,
        'order_date': order_date,
        'total_amount': f"{total_amount:.2f}",
        'status': 'Pending',
    }

    # Save to orders.csv
    csv_storage.append_record(ORDERS_FILE, order_record)

    # 5. Save all items into order_items.csv
    for item_entry in order_items_to_save:
        oi_id = csv_storage.generate_new_id(ORDER_ITEMS_FILE, 'order_item_id', prefix='OI', start_num=1001)
        item_record = {
            'order_item_id': oi_id,
            'order_id': order_id,
            'item_id': item_entry['item_id'],
            'item_name': item_entry['item_name'],
            'quantity': item_entry['quantity'],
            'unit_price': item_entry['unit_price'],
            'subtotal': item_entry['subtotal'],
        }
        csv_storage.append_record(ORDER_ITEMS_FILE, item_record)

    return True, f"Order #{order_id} placed successfully for {customer.get('name')}.", order_record


def get_all_orders(search_query: str = None, status_filter: str = None) -> list[dict]:
    """
    Get all orders with customer details attached.
    Orders are returned sorted from newest to oldest.
    """
    orders = csv_storage.read_all(ORDERS_FILE)
    customers = {c['customer_id']: c for c in customer_service.get_all_customers()}

    enriched_orders = []
    for o in orders:
        c_id = o.get('customer_id')
        cust = customers.get(c_id, {'name': 'Unknown Customer', 'phone': '-'})
        o_copy = dict(o)
        o_copy['customer_name'] = cust.get('name', 'Unknown')
        o_copy['customer_phone'] = cust.get('phone', '-')
        enriched_orders.append(o_copy)

    # Reverse so newest orders appear at top
    enriched_orders.reverse()

    # Apply filters
    if status_filter and status_filter != 'All':
        enriched_orders = [o for o in enriched_orders if o.get('status', '').lower() == status_filter.lower()]

    if search_query:
        query = search_query.strip().lower()
        enriched_orders = [
            o for o in enriched_orders
            if query in o.get('order_id', '').lower()
            or query in o.get('customer_name', '').lower()
            or query in o.get('customer_phone', '').lower()
        ]

    return enriched_orders


def get_order_by_id(order_id: str) -> dict | None:
    """
    Retrieve single order record from orders.csv.
    """
    return csv_storage.find_by_id(ORDERS_FILE, 'order_id', order_id)


def get_order_details(order_id: str) -> dict | None:
    """
    Retrieve full order details including:
    - Order summary
    - Customer information
    - List of snapshot items from order_items.csv
    """
    order = get_order_by_id(order_id)
    if not order:
        return None

    customer = customer_service.get_customer_by_id(order.get('customer_id'))
    if not customer:
        customer = {'customer_id': order.get('customer_id'), 'name': 'Unknown Customer', 'phone': '-'}

    all_items = csv_storage.read_all(ORDER_ITEMS_FILE)
    order_items = [item for item in all_items if item.get('order_id') == order_id]

    return {
        'order': order,
        'customer': customer,
        'items': order_items,
    }


def update_order_status(order_id: str, new_status: str) -> tuple[bool, str]:
    """
    Update order status to Pending, Preparing, Ready, Completed, or Cancelled.
    """
    if new_status not in VALID_STATUSES:
        return False, f"Invalid status '{new_status}'. Allowed: {', '.join(VALID_STATUSES)}"

    order = get_order_by_id(order_id)
    if not order:
        return False, f"Order #{order_id} does not exist."

    success = csv_storage.update_record(ORDERS_FILE, 'order_id', order_id, {'status': new_status})
    if success:
        return True, f"Order #{order_id} status updated to '{new_status}'."
    return False, "Failed to update order status."


def get_dashboard_stats() -> dict:
    """
    Compute real-time summary statistics strictly from CSV data.
    Rule: Cancelled orders are excluded from total sales.
    """
    customers = customer_service.get_all_customers()
    menu_items = menu_service.get_all_menu_items()
    orders = csv_storage.read_all(ORDERS_FILE)

    total_sales = Decimal('0.00')
    for order in orders:
        status = order.get('status', '').strip()
        # Cancelled orders must NOT be included in total sales
        if status.lower() != 'cancelled':
            try:
                amt = Decimal(order.get('total_amount', '0.00'))
                total_sales += amt
            except Exception:
                pass

    recent_orders = get_all_orders()[:5]

    return {
        'total_customers': len(customers),
        'total_menu_items': len(menu_items),
        'total_orders': len(orders),
        'total_sales': f"{total_sales:.2f}",
        'recent_orders': recent_orders,
    }

