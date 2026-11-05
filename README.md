# 🍽️ Restaurant Management System

A lightweight, robust web application built with **Python**, **Django**, **HTML**, and **CSS**, designed to help restaurants manage their daily counter operations. The system uses human-readable **CSV (Comma-Separated Values)** files for permanent data storage, providing a clean, transparent, and portable application without external database server overhead.

---

## 1. Project Title
**Restaurant Management System**  
*A Clean, CSV-Powered Web Application Built with Python and Django.*

---

## 2. Project Description
The **Restaurant Management System** is an easy-to-use software solution built for restaurants, cafes, and food outlets to streamline their front-desk and counter operations. 

Traditionally, small food establishments track customer orders and invoices using manual paper tickets and registers. This leads to handwriting ambiguities, calculation errors, lost order sheets, and slow billing.

This application provides a centralized web dashboard running locally on a computer. Staff can quickly register customer information, manage a categorized food menu, take multi-item customer orders, update real-time kitchen preparation statuses, and generate professional, printable receipts with a single click.

All persistent application data is saved directly in plain **CSV** files in the `data/` directory using Python's standard `csv` library. The system runs without requiring external SQL database engines (such as MySQL, SQLite, or MongoDB), making it reliable, fast to set up, and easily inspectable.

---

## 3. Project Objectives
1. **Streamline Counter Operations:** Replace physical order slips and handwritten registers with a digital dashboard.
2. **Automate Billing & Arithmetic:** Automatically calculate item subtotals, grand totals, and sales summaries using exact decimal calculations.
3. **Preserve Historical Financial Accuracy:** Freeze historical unit prices in order records so that future menu price changes never modify previous customer bills.
4. **Fast Record Lookup:** Provide instant search and filtering by customer name, phone number, order ID, and food category.
5. **Portable File-Based Storage:** Demonstrate reliable data persistence using Python's built-in file handling and atomic file writes.
6. **Clean Architecture:** Deliver a well-structured, modular codebase separating business services, storage logic, views, and templates.

---

## 4. Technologies Used

| Technology | Purpose in the Project |
| :--- | :--- |
| **Python 3** | Core language executing business logic, data validation, money calculations (`decimal` module), and CSV file handling. |
| **Django (v5+)** | Handles URL routing (`urls.py`), request processing, and HTML template rendering (`views.py`). Uses cookie-based flash messaging for alerts. |
| **HTML5** | Defines clean semantic structure for the dashboard, tables, receipt invoice, forms, and cards. |
| **CSS3** | Custom styling with a modern orange (`#ea580c`) and white color palette, responsive grid layouts, status badges, and `@media print` rules for thermal/A4 printing. Pure custom CSS without external frameworks. |
| **CSV Storage** | Four structured CSV files manage all permanent data records (`customers.csv`, `menu.csv`, `orders.csv`, and `order_items.csv`). |

---

## 5. System Features

### A. Dashboard
- **Real-Time Metrics:** Live counts calculated directly from CSV records:
  - Total Registered Customers
  - Total Menu Items
  - Total Orders Placed
  - Total Sales Revenue (in ₹ INR, excluding cancelled orders)
- **Recent Orders Table:** Displays the 5 most recent customer orders with customer name, phone number, date, time, total amount, and status badge.
- **Quick Shortcuts:** Direct navigation buttons to Place Order, Customers, Menu, Orders, and Billing.

### B. Customer Management
- **Fields:** Customer ID (auto-generated, e.g., `CUST101`), Full Name, and Phone Number.
- **Validation:** Enforces valid names (minimum 2 characters) and valid 10-digit mobile numbers.
- **Features:** Add Customer, View Table, Edit Customer, Delete Customer, and Search by name or phone.

### C. Menu Management
- **Fields:** Item ID (auto-generated, e.g., `ITEM101`), Item Name, Category, and Price (₹).
- **Categories:** Fast Food, Beverages, Snacks, Main Course, and Desserts.
- **Validation:** Non-empty item name and price strictly greater than ₹0.00.
- **Features:** Add Item, Edit Item, Delete Item, Search by name, and Filter by category.

### D. Order Management
- **Multi-Item Order Flow:**
  1. Select an existing customer.
  2. Choose a food item from the menu and enter quantity.
  3. Add multiple items to the order.
  4. View item-wise subtotals and auto-calculated final total in real-time.
  5. Place Order and record data in CSV files.
- **Price Freeze Integrity:** At the moment of order placement, item names and unit prices are permanently captured in `order_items.csv`. Subsequent menu price changes will not alter historical orders or receipts.
- **Order Statuses:** `Pending`, `Preparing`, `Ready`, `Completed`, and `Cancelled`.
- **Cancelled Orders Rule:** Cancelled orders are automatically excluded from Total Sales calculations.
- **Search & Filter:** Search by Order ID or customer name, and filter by status.

### E. Billing & Receipt Generation
- **Order Selector:** Dropdown selector to choose any existing order.
- **Professional Receipt:** Clean restaurant invoice displaying:
  - Restaurant Name, Address, Contact details, and GSTIN.
  - Receipt Number and Order ID.
  - Customer Details (Name, Phone, Customer ID).
  - Itemized table with Item Description, Unit Price, Quantity, and Subtotal.
  - Final Bill Total in ₹ INR.
- **Print Receipt:** Built-in "Print Bill Receipt" button (`window.print()`). Uses custom `@media print` CSS so all navigation bars and sidebars are hidden, printing only the clean invoice receipt.

---

## 6. Project Folder Structure

```
restaurant_management_system/
│
├── manage.py                     # Django CLI utility to run development server
├── requirements.txt               # Project dependencies (Django)
├── README.md                      # Complete documentation
├── .gitignore                     # Git ignore rules for virtual environments and cache
│
├── restaurant/                    # Project settings and root routing
│   ├── __init__.py
│   ├── settings.py                # Django configuration
│   ├── urls.py                    # Root URL router
│   ├── wsgi.py                    # WSGI entry point
│   └── asgi.py                    # ASGI entry point
│
├── management/                    # Application package
│   ├── __init__.py
│   ├── urls.py                    # URL routes for management modules
│   ├── views.py                   # Request-response views
│   ├── csv_storage.py             # CSV engine (read, write, update, atomic replace, ID generation)
│   ├── customer_service.py        # Customer validation and CRUD operations
│   ├── menu_service.py            # Menu item validation and price calculations
│   ├── order_service.py           # Order placement, price snapshots, and sales aggregation
│   └── billing_service.py         # Bill formatting, item aggregation, and calculations
│
├── templates/                     # HTML templates
│   ├── base.html                  # Master layout with sidebar navigation
│   ├── dashboard.html             # Dashboard with stat cards and recent orders
│   ├── customers.html             # Customer management page
│   ├── menu.html                  # Menu items management page
│   ├── orders.html                # Orders list and status manager
│   ├── order_create.html          # Interactive multi-item order placement
│   ├── order_details.html         # Individual order item breakdown
│   └── billing.html               # Printable restaurant invoice
│
├── static/                        # Static files
│   └── css/
│       └── style.css              # Custom orange-and-white theme & print styles
│
└── data/                          # Permanent CSV data files
    ├── customers.csv              # Customer records
    ├── menu.csv                   # Food menu list
    ├── orders.csv                 # Master orders
    └── order_items.csv            # Line items with snapshot unit prices
```

---

## 7. Application Workflow

### High-Level Request Flow
```
[User Browser (Chrome)]
       │
       ▼ (HTTP Request)
[Django URL Router (restaurant/urls.py & management/urls.py)]
       │
       ▼
[Management View Function (management/views.py)]
       │
       ▼ (Calls Service Layer)
[Service Layer (customer_service / menu_service / order_service / billing_service)]
       │
       ▼ (Reads / Writes Records)
[CSV Storage Engine (csv_storage.py)]
       │
       ▼ (Standard Library csv module)
[CSV Files in data/ Directory (*.csv)]
       │
       ▼ (Data Returned to View)
[Django Template Engine (templates/*.html)]
       │
       ▼ (HTML + CSS Response)
[User Browser (Chrome Display)]
```

### Complete End-to-End Workflow:
1. **Add Customer:** Register the customer's name and 10-digit phone number. `customer_service.py` assigns a unique `customer_id` (e.g., `CUST101`) and saves it to `customers.csv`.
2. **Maintain Menu:** Items and current prices are maintained in `menu.csv`.
3. **Place Order:**
   - Select the customer from the dropdown.
   - Select menu items and quantities.
   - The interface computes item-wise subtotals and live grand total.
   - Staff confirms the order.
4. **Data Persistence & Price Freezing:**
   - A unique `order_id` (e.g., `ORD1001`) is generated.
   - The master order record is saved in `orders.csv` with status `Pending`.
   - Each item's current unit price and name are permanently saved in `order_items.csv`.
5. **Update Status:** Staff updates the order status through `Pending` -> `Preparing` -> `Ready` -> `Completed`.
6. **Generate & Print Bill:** Staff selects the order in Billing, reviews the itemized receipt, and clicks **Print Bill Receipt** to print or export as PDF.

---

## 8. CSV Data Storage Explanation

### What is CSV?
**CSV** (Comma-Separated Values) is a plain-text format used to store structured tabular data. Each line in a CSV file corresponds to one record, with individual fields separated by commas.

### Why CSV is Used Here:
- **Zero Server Setup:** No database servers, background daemons, or port configurations are needed.
- **Portability:** Data files can be easily copied, backed up, or opened in spreadsheet software like Microsoft Excel or Google Sheets.
- **Human Readable:** Data is stored in plain, inspectable text.

### Atomic Writes for Data Safety:
To prevent partial writes or file corruption, `csv_storage.py` uses **atomic file replacement**:
1. When modifying or deleting records, the updated data is first written to a temporary file in the same directory.
2. Once writing finishes successfully, the temporary file replaces the target CSV file atomically using Python's `Path.replace()`.

### CSV Schemas & Relationships:
The four CSV files are linked using relational IDs:
- `orders.csv` references `customers.csv` via `customer_id`.
- `order_items.csv` references `orders.csv` via `order_id`.
- `order_items.csv` references `menu.csv` via `item_id`.

#### Sample Headers & Records:

**`data/customers.csv`**
```csv
customer_id,name,phone
CUST101,Rahul Sharma,9876543210
CUST102,Priya Patel,9123456780
```

**`data/menu.csv`**
```csv
item_id,item_name,category,price
ITEM101,Burger,Fast Food,100.00
ITEM102,Pizza,Fast Food,200.00
ITEM103,Sandwich,Snacks,80.00
ITEM104,Cold Coffee,Beverages,90.00
```

**`data/orders.csv`**
```csv
order_id,customer_id,order_date,total_amount,status
ORD1001,CUST101,2026-11-04 13:15,390.00,Completed
ORD1002,CUST102,2026-11-04 14:30,280.00,Ready
```

**`data/order_items.csv`**
```csv
order_item_id,order_id,item_id,item_name,quantity,unit_price,subtotal
OI1001,ORD1001,ITEM101,Burger,1,100.00,100.00
OI1002,ORD1001,ITEM102,Pizza,1,200.00,200.00
OI1003,ORD1001,ITEM104,Cold Coffee,1,90.00,90.00
```

---

## 9. Installation Requirements
- **Python 3.10+** (Python 3.10, 3.11, 3.12, 3.13, 3.14).
- **pip** (Python package installer).
- **Google Chrome** (or any modern web browser).
- *(Optional)* A code editor like VS Code or PyCharm.

---

## 10. How to Run the Project

### On macOS / Linux:
```bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Start the development server
python3 manage.py runserver
```

### On Windows:
```cmd
:: 1. Create a virtual environment
py -m venv venv

:: 2. Activate virtual environment
venv\Scripts\activate

:: 3. Install requirements
pip install -r requirements.txt

:: 4. Start the development server
py manage.py runserver
```

### Open the Application:
Open Google Chrome and visit:  
👉 **`http://127.0.0.1:8000/`**

### Stop the Server:
Press **`CTRL + C`** in the terminal to stop the server.

---

## 11. Sample Data Included
The application includes pre-loaded sample data:
- **5 Customers:** Rahul Sharma, Priya Patel, Amit Kumar, Sneha Verma, Vikram Singh.
- **8 Menu Items:** Burger (₹100), Pizza (₹200), Sandwich (₹80), Cold Coffee (₹90), French Fries (₹70), Veg Noodles (₹120), Paneer Tikka (₹180), Chocolate Shake (₹110).
- **5 Orders:** With varying statuses (Completed, Ready, Preparing, Cancelled, Pending) to demonstrate status management and revenue calculations immediately.

---

## 12. Testing Checklist

- [x] **Dashboard:** Verify live metrics for customers, menu items, orders, and sales.
- [x] **Customer CRUD:** Add, view, edit, search by name/phone, and delete customer records.
- [x] **Menu CRUD:** Add, edit, category filter, and delete menu items with price validation.
- [x] **Multi-Item Order Placement:** Place an order with multiple items; verify subtotals and grand total.
- [x] **Historical Price Snapshot:** Verify that changing a menu item's price does not alter past orders or previous receipts.
- [x] **Cancelled Order Rule:** Verify that cancelled orders are excluded from total sales revenue.
- [x] **Billing & Print:** Open receipt for an order and test print view with `window.print()`.

---

## 13. System Limitations
1. **Single-Node Local Storage:** Records are stored in local flat files. The system is designed for single-workstation counter use without concurrent distributed database locking.
2. **Local Storage Persistence:** Data lives inside the `data/` folder. Deleting these files resets the application data.
3. **No Online Payment Gateway:** Designed for physical counter settlement (cash, card, counter QR/UPI) rather than online payment gateway integrations.

---

## 14. Future Improvements
- User authentication and role-based permissions (Cashier vs Manager).
- Migration option to an external database (PostgreSQL/MySQL) via Django ORM if scaling.
- Kitchen Display Screen (KDS) with live WebSocket order updates.
- Export sales reports to PDF and Excel formats.

---

## 15. Technical Questions and Answers

### Q1: What role does Django play in this application?
**Ans:** Django acts as the web controller and routing engine. It maps incoming HTTP requests to views, processes submitted form data, interacts with service modules, and renders HTML templates.

### Q2: Why are CSV files used instead of an SQL database?
**Ans:** CSV files are lightweight, transparent, human-readable, and require no database servers or drivers. They run out-of-the-box using Python's standard `csv` library.

### Q3: How is file corruption prevented during CSV write operations?
**Ans:** By using atomic file replacement. Updates are written to a temporary file first; once writing is verified complete, the file is atomically renamed to replace the target file.

### Q4: Why is `unit_price` stored in `order_items.csv`?
**Ans:** If the menu price of a food item changes in the future, past orders and historical invoices must retain the price at which the order was placed. Storing the unit price snapshot in `order_items.csv` ensures financial record integrity.

### Q5: How are Cancelled orders handled in Total Sales?
**Ans:** The sales calculation function reads `orders.csv` and skips any order with a status of `Cancelled`, ensuring that only valid orders contribute to reported revenue.

### Q6: Why is Python's `Decimal` module used instead of `float` for prices?
**Ans:** Floats introduce binary rounding inaccuracies. `Decimal` provides exact fixed-point arithmetic required for financial and billing calculations.

### Q7: How does the application generate unique IDs (e.g., CUST101, ORD1001)?
**Ans:** The `generate_new_id()` function scans existing IDs in the target CSV, extracts the highest numeric value, and increments it by 1 for the new record.

### Q8: How does the Print Bill functionality work?
**Ans:** The "Print Bill Receipt" button triggers `window.print()`. Custom `@media print` CSS rules hide sidebars, headers, and action buttons, leaving only the clean receipt to print or save as PDF.

---

**License:** Free & Open Source for Educational and Commercial Reference
# python_project_restaurant
