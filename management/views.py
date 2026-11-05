"""
views.py - Request handling and controller views for Restaurant Management System.

All views use pure Django standard features, service layer methods,
and Cookie-backed messages. No database or ORM is used.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from . import customer_service
from . import menu_service
from . import order_service
from . import billing_service


# ==========================================
# 1. DASHBOARD VIEW
# ==========================================
def dashboard_view(request):
    """
    Renders the main dashboard with statistics and recent orders.
    All figures are calculated strictly from CSV files.
    """
    stats = order_service.get_dashboard_stats()
    context = {
        'active_page': 'dashboard',
        'stats': stats,
    }
    return render(request, 'dashboard.html', context)


# ==========================================
# 2. CUSTOMER MANAGEMENT VIEWS
# ==========================================
def customer_list_view(request):
    """
    Handles viewing, searching, adding, and editing customers.
    Customer fields are strictly: customer_id, name, phone.
    """
    search_query = request.GET.get('q', '').strip()
    edit_id = request.GET.get('edit', '').strip()

    # Handle form submissions (Add or Edit)
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()

        if action == 'add':
            success, msg, _ = customer_service.add_customer(name, phone)
            if success:
                messages.success(request, msg)
                return redirect('customer_list')
            else:
                messages.error(request, msg)

        elif action == 'edit':
            target_id = request.POST.get('customer_id', '').strip()
            success, msg = customer_service.update_customer(target_id, name, phone)
            if success:
                messages.success(request, msg)
                return redirect('customer_list')
            else:
                messages.error(request, msg)

    # Fetch customer list and optional edit record
    customers = customer_service.get_all_customers(search_query)
    customer_to_edit = customer_service.get_customer_by_id(edit_id) if edit_id else None

    context = {
        'active_page': 'customers',
        'customers': customers,
        'search_query': search_query,
        'customer_to_edit': customer_to_edit,
        'total_count': len(customers),
    }
    return render(request, 'customers.html', context)


def customer_delete_view(request, customer_id):
    """
    Deletes a customer by ID from customers.csv.
    """
    if request.method == 'POST':
        success, msg = customer_service.delete_customer(customer_id)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)
    return redirect('customer_list')


# ==========================================
# 3. MENU MANAGEMENT VIEWS
# ==========================================
def menu_list_view(request):
    """
    Handles viewing, searching, adding, and editing food menu items.
    Menu fields: item_id, item_name, category, price.
    """
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    edit_id = request.GET.get('edit', '').strip()

    if request.method == 'POST':
        action = request.POST.get('action')
        item_name = request.POST.get('item_name', '').strip()
        category = request.POST.get('category', '').strip()
        price = request.POST.get('price', '').strip()

        if action == 'add':
            success, msg, _ = menu_service.add_menu_item(item_name, category, price)
            if success:
                messages.success(request, msg)
                return redirect('menu_list')
            else:
                messages.error(request, msg)

        elif action == 'edit':
            item_id = request.POST.get('item_id', '').strip()
            success, msg = menu_service.update_menu_item(item_id, item_name, category, price)
            if success:
                messages.success(request, msg)
                return redirect('menu_list')
            else:
                messages.error(request, msg)

    menu_items = menu_service.get_all_menu_items(search_query, category_filter)
    item_to_edit = menu_service.get_menu_item_by_id(edit_id) if edit_id else None

    context = {
        'active_page': 'menu',
        'menu_items': menu_items,
        'categories': menu_service.CATEGORIES,
        'selected_category': category_filter,
        'search_query': search_query,
        'item_to_edit': item_to_edit,
        'total_count': len(menu_items),
    }
    return render(request, 'menu.html', context)


def menu_delete_view(request, item_id):
    """
    Deletes a menu item by ID from menu.csv.
    """
    if request.method == 'POST':
        success, msg = menu_service.delete_menu_item(item_id)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)
    return redirect('menu_list')


# ==========================================
# 4. ORDER MANAGEMENT VIEWS
# ==========================================
def order_list_view(request):
    """
    Displays all orders with customer details, order statuses, and search filter.
    """
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    orders = order_service.get_all_orders(search_query, status_filter)

    context = {
        'active_page': 'orders',
        'orders': orders,
        'statuses': order_service.VALID_STATUSES,
        'selected_status': status_filter,
        'search_query': search_query,
        'total_count': len(orders),
    }
    return render(request, 'orders.html', context)


def order_create_view(request):
    """
    Order creation flow:
    1. Select an existing customer.
    2. Select food item and quantity.
    3. Add multiple items.
    4. Auto-calculate subtotals and grand total.
    5. Save order in orders.csv and snapshot items in order_items.csv.
    """
    customers = customer_service.get_all_customers()
    menu_items = menu_service.get_all_menu_items()

    if request.method == 'POST':
        customer_id = request.POST.get('customer_id', '').strip()
        item_ids = request.POST.getlist('item_id[]')
        quantities = request.POST.getlist('quantity[]')

        # Combine into item list
        raw_items = []
        for i_id, qty in zip(item_ids, quantities):
            if i_id and qty:
                raw_items.append({'item_id': i_id, 'quantity': qty})

        success, msg, order_record = order_service.place_order(customer_id, raw_items)
        if success:
            messages.success(request, msg)
            return redirect(f"{reverse('billing')}?order_id={order_record['order_id']}")
        else:
            messages.error(request, msg)

    context = {
        'active_page': 'order_create',
        'customers': customers,
        'menu_items': menu_items,
    }
    return render(request, 'order_create.html', context)


def order_details_view(request, order_id):
    """
    View individual order details with items, historical prices, and customer info.
    """
    details = order_service.get_order_details(order_id)
    if not details:
        messages.error(request, f"Order #{order_id} not found.")
        return redirect('order_list')

    context = {
        'active_page': 'orders',
        'order': details['order'],
        'customer': details['customer'],
        'items': details['items'],
        'statuses': order_service.VALID_STATUSES,
    }
    return render(request, 'order_details.html', context)


def order_status_update_view(request, order_id):
    """
    Update order status (Pending, Preparing, Ready, Completed, Cancelled).
    """
    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip()
        success, msg = order_service.update_order_status(order_id, new_status)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)

    # Redirect back to where the request came from
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('order_details', order_id=order_id)


# ==========================================
# 5. BILLING MANAGEMENT VIEWS
# ==========================================
def billing_view(request, order_id=None):
    """
    Display printable restaurant bill/invoice for an existing order.
    Includes an order selector to pick any order from the system.
    """
    # Accept order_id either from URL path or GET query parameter
    if not order_id:
        order_id = request.GET.get('order_id', '').strip()

    all_orders = billing_service.get_all_orders_for_billing()

    # If no order selected yet, default to the latest order if available
    if not order_id and all_orders:
        order_id = all_orders[0].get('order_id')

    bill_data = billing_service.prepare_bill(order_id) if order_id else None

    context = {
        'active_page': 'billing',
        'all_orders': all_orders,
        'selected_order_id': order_id,
        'bill': bill_data,
    }
    return render(request, 'billing.html', context)

