# 🍽️ Restaurant Management System

A modern, lightweight, and fully responsive web application built with **Python**, **Django**, **HTML5**, and **CSS3**. The system manages end-to-end counter operations for restaurants, cafes, and food outlets.

All permanent application data is saved directly in plain **CSV (Comma-Separated Values)** files with **zero external database dependencies** (no SQLite, MySQL, or PostgreSQL required). The application is optimized for both local desktop use and one-click cloud deployment on platforms like **Vercel**.

---

## 📱 Fully Responsive Design (Mobile, Tablet, Desktop)

The entire user interface is built with custom CSS and vanilla JavaScript to provide a native-feeling experience across all screen sizes:

- **Mobile Navigation Drawer (`<= 820px`):** The sidebar transforms into a slide-out mobile drawer accessed via a hamburger menu button (`☰`) in the topbar, complete with a backdrop blur overlay and auto-closing links upon navigation.
- **Adaptive Layout Grids:** Executive stat cards, customer forms, menu editors, and order summary views automatically reflow from multi-column grids to finger-friendly vertical stacks on mobile phones and tablets.
- **Scroll-Protected Tables:** All data tables are wrapped in smooth touch-scrolling containers (`-webkit-overflow-scrolling: touch`) so tabular records never crunch on narrow screens.
- **Mobile Touch Controls:** Dropdowns, quantity adjusters, "+ Add Item" buttons, and "Place Order" controls expand to full touch-target widths on smartphones.
- **Print Optimization (`@media print`):** Clicking "Print Bill Receipt" hides all sidebars, navigation controls, and screen buttons, outputting only the pristine restaurant invoice on A4 or thermal receipt printers.

---

## 🚀 Key Features

### 1. Executive Dashboard
- **Live CSV Metric Cards:** Real-time computation of:
  - Total Registered Customers
  - Total Menu Items
  - Total Orders Placed
  - Total Sales Revenue (in ₹ INR, automatically excluding cancelled orders)
- **Recent Orders Table:** Shows the latest 5 orders with customer name, phone, date, time, total amount, and status badges.
- **Quick Shortcuts:** Direct access to Place Order, Customer Management, Food Menu, Orders List, and Billing.

### 2. Customer Management
- **Strict Data Fields:** `customer_id` (auto-generated, e.g., `CUST101`), `name`, and `phone`.
- **Validation:** Enforces minimum 2-character names and valid 10-digit mobile numbers.
- **Features:** Add Customer, View Table, Edit Customer, Delete Customer with confirmation, and real-time Search by name or phone.

### 3. Food Menu Management
- **Fields:** `item_id` (auto-generated, e.g., `ITEM101`), `item_name`, `category`, and `price`.
- **Categories:** Fast Food, Beverages, Snacks, Main Course, and Desserts.
- **Validation:** Non-empty food item names and prices strictly greater than ₹0.00.
- **Features:** Add Item, Edit Item, Delete Item, Search by name, and Filter by category dropdown.

### 4. Interactive Order Management
- **Multi-Item Order Flow:**
  1. Select an existing customer from the dropdown.
  2. Select food item and quantity, then tap **+ Add Item**.
  3. Add multiple items to the same order.
  4. Real-time item subtotal calculation and live grand total display.
  5. Place Order and record data in CSV files.
- **Price Freeze Integrity:** At the moment of order placement, item names and unit prices are permanently captured in `order_items.csv`. Subsequent menu price changes will **never** alter historical orders or previous customer receipts.
- **Status Lifecycle:** `Pending` ➔ `Preparing` ➔ `Ready` ➔ `Completed` (or `Cancelled`).
- **Revenue Integrity:** Cancelled orders are automatically deducted/excluded from Total Sales calculations.

### 5. Billing & Invoice Receipt
- **Order Selector:** Dropdown to pull up and view any existing order.
- **Restaurant Invoice Layout:** Displays restaurant name, address, GSTIN, receipt number, order date/time, customer details, itemized table, and final total in ₹ INR.
- **Browser Print Functionality:** Built-in "Print Bill Receipt" button triggers `window.print()` with custom print styling.

---

## 🛠️ Technologies Used

| Technology | Purpose in Project |
| :--- | :--- |
| **Python 3** | Core language executing business logic, validation, money arithmetic (`decimal` module), and CSV file handling. |
| **Django (v5+)** | Handles URL routing, request processing, template rendering, and cookie-based flash alerts (`DATABASES = {}`). |
| **WhiteNoise** | High-performance static file serving engine for production and serverless environments. |
| **HTML5 & CSS3** | Clean semantic structure and custom orange-and-white theme (`#ea580c`), fully responsive without third-party CSS frameworks. |
| **CSV Files** | Persistent data storage engine using Python's standard `csv.DictReader` and `csv.DictWriter`. |

---

## 📁 Project Folder Structure

```
restaurant_management_system/
│
├── manage.py                     # Django development server CLI utility
├── requirements.txt               # Dependencies (Django, WhiteNoise)
├── README.md                      # Comprehensive project documentation
├── .gitignore                     # Git ignore rules
├── build_files.sh                 # Vercel deployment build script
├── vercel.json                    # Vercel deployment configuration
│
├── restaurant/                    # Main Django configuration package
│   ├── __init__.py
│   ├── settings.py                # Django settings (WhiteNoise, zero-database configuration)
│   ├── urls.py                    # Root URL router & dedicated static CSS serving endpoint
│   ├── wsgi.py                    # WSGI entry point (aliased as app for Vercel)
│   └── asgi.py                    # ASGI entry point
│
├── management/                    # Application package
│   ├── __init__.py
│   ├── urls.py                    # Routes for dashboard, customers, menu, orders, billing
│   ├── views.py                   # Request-response views
│   ├── csv_storage.py             # CSV engine (atomic writes, ID generator, /tmp fallback)
│   ├── customer_service.py        # Customer validation and CRUD operations
│   ├── menu_service.py            # Menu item validation and price calculations
│   ├── order_service.py           # Order placement, price snapshots, and sales aggregation
│   └── billing_service.py         # Bill formatting, item aggregation, and receipt calculations
│
├── templates/                     # HTML5 templates
│   ├── base.html                  # Master layout with responsive mobile navigation drawer
│   ├── dashboard.html             # Metric cards and recent orders overview
│   ├── customers.html             # Customer management page
│   ├── menu.html                  # Menu management page
│   ├── orders.html                # Orders list and status manager
│   ├── order_create.html          # Interactive multi-item order placement
│   ├── order_details.html         # Individual order item breakdown
│   ├── billing.html               # Printable restaurant invoice
│   └── includes/
│       └── style.css              # Embedded master stylesheet for instantaneous rendering
│
├── static/                        # Static assets
│   └── css/
│       └── style.css              # Master responsive stylesheet
│
├── staticfiles/                   # Production collected static files for Vercel CDN
│   ├── css/style.css
│   └── static/css/style.css
│
└── data/                          # Permanent CSV storage
    ├── customers.csv              # Customer records
    ├── menu.csv                   # Food menu list
    ├── orders.csv                 # Master orders
    └── order_items.csv            # Line items with snapshot unit prices
```

---

## 💾 CSV Data Storage Explanation

### Data Architecture:
All records are saved in structured CSV files inside the `data/` folder:
- **`customers.csv`:** Stores `customer_id`, `name`, `phone`.
- **`menu.csv`:** Stores `item_id`, `item_name`, `category`, `price`.
- **`orders.csv`:** Stores `order_id`, `customer_id`, `order_date`, `total_amount`, `status`.
- **`order_items.csv`:** Stores `order_item_id`, `order_id`, `item_id`, `item_name`, `quantity`, `unit_price`, `subtotal`.

### Atomic Writes for Data Safety:
When updating or deleting records, `csv_storage.py` writes the updated data to a temporary file first, then atomically replaces the target file via `Path.replace()`. This prevents partial writes or file corruption if a request is interrupted.

### Serverless Compatibility (`/tmp` Fallback):
On serverless platforms like Vercel where the deployment directory is read-only, `csv_storage.py` automatically detects the environment and uses `/tmp/restaurant_data`, copying starter files on initial boot. This ensures write operations (adding customers, creating orders, updating menu items) succeed seamlessly in cloud environments.

---

## 💻 How to Run Locally

### For macOS / Linux:
```bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Start the Django development server
python3 manage.py runserver
```

### For Windows:
```cmd
:: 1. Create a virtual environment
py -m venv venv

:: 2. Activate virtual environment
venv\Scripts\activate

:: 3. Install requirements
pip install -r requirements.txt

:: 4. Start the Django development server
py manage.py runserver
```

### Access in Browser:
Open Google Chrome and visit:  
👉 **`http://127.0.0.1:8000/`**

To stop the server at any time, press **`CTRL + C`** in your terminal.

---

## ☁️ How to Deploy on Vercel

The repository is pre-configured for Vercel deployment:
1. Push this project to your GitHub repository.
2. Go to [Vercel](https://vercel.com/) and click **Add New > Project**.
3. Import your GitHub repository (`python_project_restaurant`).
4. Click **Deploy**. Vercel will install dependencies from `requirements.txt`, run `build_files.sh`, gather static assets, and deploy the application to your production URL.

---

## ❓ Frequently Asked Questions (FAQ)

**Q: How does the application function without a database?**  
A: Django is configured with `DATABASES = {}`. All CRUD operations are executed directly against CSV files using Python's built-in `csv` module with atomic file replacements.

**Q: Why do historical bills remain unchanged when menu prices update?**  
A: When an order is placed, `order_service.py` freezes the current food name and unit price inside `order_items.csv`. Past orders calculate totals from this historical snapshot rather than reading live menu prices.

**Q: How are cancelled orders handled in sales metrics?**  
A: The dashboard calculation reads `orders.csv` and skips orders with status `Cancelled`, ensuring that only completed and active orders contribute to reported sales revenue.

**Q: What prevents CSS MIME type errors on cloud platforms?**  
A: The master stylesheet is embedded directly into the base template (`templates/includes/style.css`), while simultaneously supported by WhiteNoise and an explicit Django static view at `/static/css/style.css`.
