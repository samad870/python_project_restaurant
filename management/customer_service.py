"""
customer_service.py - Customer business logic and validation.

Fields:
- customer_id: Unique identifier (e.g., CUST101)
- name: Customer full name
- phone: 10-digit mobile number

Rules:
- Customer fields must ONLY be: customer_id, name, phone.
- Prevent empty customer names.
- Validate phone numbers (must be valid 10 digits).
"""

import re
from . import csv_storage

FILENAME = 'customers.csv'
ID_FIELD = 'customer_id'


def validate_customer_data(name: str, phone: str) -> tuple[bool, str]:
    """
    Validate customer name and phone number.
    Returns (True, '') if valid, or (False, 'error description') if invalid.
    """
    clean_name = name.strip() if name else ''
    clean_phone = phone.strip() if phone else ''

    # Validate name
    if not clean_name:
        return False, "Customer name cannot be empty."
    if len(clean_name) < 2:
        return False, "Customer name must be at least 2 characters long."

    # Validate phone (remove optional hyphens or spaces if entered)
    sanitized_phone = re.sub(r'[\s\-]', '', clean_phone)
    if not sanitized_phone.isdigit() or len(sanitized_phone) != 10:
        return False, "Phone number must be a valid 10-digit numeric number."

    return True, sanitized_phone


def get_all_customers(search_query: str = None) -> list[dict]:
    """
    Retrieve all customers, optionally filtered by name or phone query.
    """
    customers = csv_storage.read_all(FILENAME)
    if not search_query:
        return customers

    query = search_query.strip().lower()
    return [
        c for c in customers
        if query in c.get('name', '').lower() or query in c.get('phone', '').lower()
    ]


def get_customer_by_id(customer_id: str) -> dict | None:
    """
    Fetch a customer by customer_id.
    """
    return csv_storage.find_by_id(FILENAME, ID_FIELD, customer_id)


def add_customer(name: str, phone: str) -> tuple[bool, str, dict | None]:
    """
    Validate and save a new customer to customers.csv.
    Generates a unique customer_id like CUST101, CUST102.
    Returns (success, message, customer_dict).
    """
    is_valid, sanitized_or_err = validate_customer_data(name, phone)
    if not is_valid:
        return False, sanitized_or_err, None

    clean_name = name.strip()
    clean_phone = sanitized_or_err

    # Check if a customer with the same phone already exists
    existing = get_all_customers()
    for cust in existing:
        if cust.get('phone') == clean_phone:
            return False, f"A customer with phone number {clean_phone} already exists ({cust.get('name')}).", None

    new_id = csv_storage.generate_new_id(FILENAME, ID_FIELD, prefix='CUST', start_num=101)
    record = {
        'customer_id': new_id,
        'name': clean_name,
        'phone': clean_phone,
    }
    csv_storage.append_record(FILENAME, record)
    return True, f"Customer '{clean_name}' added successfully with ID {new_id}.", record


def update_customer(customer_id: str, name: str, phone: str) -> tuple[bool, str]:
    """
    Validate and update an existing customer's name and phone.
    """
    is_valid, sanitized_or_err = validate_customer_data(name, phone)
    if not is_valid:
        return False, sanitized_or_err

    clean_name = name.strip()
    clean_phone = sanitized_or_err

    # Ensure customer exists
    customer = get_customer_by_id(customer_id)
    if not customer:
        return False, f"Customer with ID {customer_id} does not exist."

    # Check if new phone belongs to another customer
    existing = get_all_customers()
    for cust in existing:
        if cust.get('customer_id') != customer_id and cust.get('phone') == clean_phone:
            return False, f"Phone number {clean_phone} is already registered to another customer."

    updated_data = {
        'name': clean_name,
        'phone': clean_phone,
    }
    success = csv_storage.update_record(FILENAME, ID_FIELD, customer_id, updated_data)
    if success:
        return True, f"Customer {customer_id} updated successfully."
    return False, "Failed to update customer record."


def delete_customer(customer_id: str) -> tuple[bool, str]:
    """
    Delete a customer from customers.csv.
    """
    customer = get_customer_by_id(customer_id)
    if not customer:
        return False, f"Customer with ID {customer_id} not found."

    success = csv_storage.delete_record(FILENAME, ID_FIELD, customer_id)
    if success:
        return True, f"Customer {customer_id} ({customer.get('name')}) deleted successfully."
    return False, "Failed to delete customer."

