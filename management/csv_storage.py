"""
csv_storage.py - Core CSV storage engine for Restaurant Management System.

This module provides reusable, safe helper functions to:
- Automatically initialize CSV storage directory and files with headers.
- Read records as Python dictionaries using csv.DictReader.
- Write and append records safely using csv.DictWriter.
- Update and delete records safely using atomic file replacement.
- Generate unique sequential IDs (e.g., CUST101, ITEM101, ORD1001).
"""

import os
import csv
import tempfile
from pathlib import Path
from django.conf import settings

# Directory where CSV files are saved
DATA_DIR = Path(getattr(settings, 'DATA_DIR', Path(__file__).resolve().parent.parent / 'data'))

# Schema definition for all CSV files
CSV_SCHEMAS = {
    'customers.csv': ['customer_id', 'name', 'phone'],
    'menu.csv': ['item_id', 'item_name', 'category', 'price'],
    'orders.csv': ['order_id', 'customer_id', 'order_date', 'total_amount', 'status'],
    'order_items.csv': ['order_item_id', 'order_id', 'item_id', 'item_name', 'quantity', 'unit_price', 'subtotal'],
}


def get_file_path(filename: str) -> Path:
    """Return the absolute Path for a given CSV filename inside data/."""
    return DATA_DIR / filename


def init_storage():
    """
    Ensure the data/ directory exists and all required CSV files
    are initialized with their proper headers.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename, headers in CSV_SCHEMAS.items():
        file_path = get_file_path(filename)
        if not file_path.exists() or file_path.stat().st_size == 0:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)


def read_all(filename: str) -> list[dict]:
    """
    Read all rows from a CSV file and return them as a list of dictionaries.
    If the file does not exist, initialize storage first.
    """
    init_storage()
    file_path = get_file_path(filename)

    records = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Strip extra whitespaces from values
                cleaned_row = {k.strip(): (v.strip() if v is not None else '') for k, v in row.items()}
                records.append(cleaned_row)
    except FileNotFoundError:
        init_storage()
    return records


def write_all(filename: str, records: list[dict], fieldnames: list[str] = None):
    """
    Write a list of dictionaries to a CSV file atomically.
    Atomic write uses a temporary file and replaces the target file,
    ensuring that no data is lost or corrupted if an error occurs mid-write.
    """
    init_storage()
    if fieldnames is None:
        fieldnames = CSV_SCHEMAS.get(filename, [])

    file_path = get_file_path(filename)

    # Write to a temporary file in the same directory first
    temp_dir = file_path.parent
    with tempfile.NamedTemporaryFile(mode='w', newline='', encoding='utf-8', dir=temp_dir, delete=False) as tmp:
        writer = csv.DictWriter(tmp, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for record in records:
            writer.writerow(record)
        temp_path = Path(tmp.name)

    # Atomically replace target file
    temp_path.replace(file_path)


def append_record(filename: str, record: dict):
    """
    Append a single record (dictionary) to the specified CSV file.
    """
    init_storage()
    fieldnames = CSV_SCHEMAS.get(filename, list(record.keys()))
    file_path = get_file_path(filename)

    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writerow(record)


def find_by_id(filename: str, id_field: str, target_id: str) -> dict | None:
    """
    Find and return a single record where id_field matches target_id.
    Returns None if not found.
    """
    records = read_all(filename)
    target_id_str = str(target_id).strip()
    for record in records:
        if record.get(id_field, '').strip() == target_id_str:
            return record
    return None


def update_record(filename: str, id_field: str, target_id: str, updated_data: dict) -> bool:
    """
    Update an existing record in the CSV file by matching id_field.
    Returns True if updated, False if record was not found.
    """
    records = read_all(filename)
    target_id_str = str(target_id).strip()
    found = False

    for record in records:
        if record.get(id_field, '').strip() == target_id_str:
            record.update(updated_data)
            # Ensure the ID itself is not altered accidentally
            record[id_field] = target_id_str
            found = True
            break

    if found:
        write_all(filename, records, CSV_SCHEMAS.get(filename))
    return found


def delete_record(filename: str, id_field: str, target_id: str) -> bool:
    """
    Delete a record from the CSV file where id_field matches target_id.
    Returns True if deleted, False if record was not found.
    """
    records = read_all(filename)
    target_id_str = str(target_id).strip()
    initial_length = len(records)

    filtered_records = [r for r in records if r.get(id_field, '').strip() != target_id_str]

    if len(filtered_records) < initial_length:
        write_all(filename, filtered_records, CSV_SCHEMAS.get(filename))
        return True
    return False


def generate_new_id(filename: str, id_field: str, prefix: str = 'ID', start_num: int = 101) -> str:
    """
    Generate the next sequential unique ID.
    Example: If CUST101, CUST102 exist, this returns CUST103.
    If no records exist, this returns CUST101.
    """
    records = read_all(filename)
    max_num = start_num - 1

    for r in records:
        val = r.get(id_field, '').strip()
        # Extract digits from the existing ID string
        digits = ''.join(c for c in val if c.isdigit())
        if digits:
            try:
                num = int(digits)
                if num > max_num:
                    max_num = num
            except ValueError:
                pass

    return f"{prefix}{max_num + 1}"

