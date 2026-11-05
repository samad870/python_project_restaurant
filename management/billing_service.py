"""
billing_service.py - Bill generation, formatting, and receipt calculations.

Provides:
- Restaurant details (Name, Address, School Project Tag)
- Itemized breakdown of order items, historical prices, and quantities
- Grand total calculation
- Helper to prepare clean bill data for HTML/print rendering
"""

from decimal import Decimal
from . import order_service


RESTAURANT_INFO = {
    'name': 'The Golden Spoon Restaurant',
    'tagline': 'Fresh Food • Warm Hospitality',
    'address': 'Main Market Road, Sector 14, New Delhi - 110001',
    'phone': '+91 98765 43210',
    'gstin': '07AAAAA0000A1Z5',
}


def prepare_bill(order_id: str) -> dict | None:
    """
    Generate complete structured bill data for the given order_id.
    """
    details = order_service.get_order_details(order_id)
    if not details:
        return None

    order = details['order']
    customer = details['customer']
    raw_items = details['items']

    bill_items = []
    subtotal = Decimal('0.00')

    for idx, item in enumerate(raw_items, start=1):
        try:
            qty = int(item.get('quantity', 1))
            unit_price = Decimal(item.get('unit_price', '0.00'))
            item_subtotal = Decimal(item.get('subtotal', str(qty * unit_price)))
        except Exception:
            qty = 1
            unit_price = Decimal('0.00')
            item_subtotal = Decimal('0.00')

        subtotal += item_subtotal

        bill_items.append({
            's_no': idx,
            'item_id': item.get('item_id'),
            'item_name': item.get('item_name'),
            'quantity': qty,
            'unit_price': f"{unit_price:.2f}",
            'subtotal': f"{item_subtotal:.2f}",
        })

    # Total bill amount
    final_total = Decimal(order.get('total_amount', f"{subtotal:.2f}"))

    return {
        'restaurant': RESTAURANT_INFO,
        'bill_no': f"BILL-{order.get('order_id')}",
        'order': order,
        'customer': customer,
        'items': bill_items,
        'subtotal': f"{subtotal:.2f}",
        'final_total': f"{final_total:.2f}",
        'is_cancelled': order.get('status', '').lower() == 'cancelled',
    }


def get_all_orders_for_billing() -> list[dict]:
    """
    Return all orders list formatted for the billing order selection dropdown.
    """
    return order_service.get_all_orders()

