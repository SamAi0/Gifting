# **Soham Gift - Backend (Django)**

This is the robust Django-based backend for the Soham Gift platform, providing a clean REST API and comprehensive administrative tools.

---

## 🛠️ **Management & Maintenance Scripts**

The backend includes several specialized scripts to maintain data integrity and synchronize with the frontend branding engine.

### **1. `sync_customization.py`**
- **Purpose**: Synchronizes branding zones from `frontend/src/data/customization.json` to the Django database.
- **Usage**:
  ```bash
  python sync_customization.py
  ```
- **Note**: It matches products by **slug** for maximum stability.

### **2. `seed_products.py`**
- **Purpose**: Seeds the database with initial products, categories, and standardized image paths.
- **Usage**:
  ```bash
  python seed_products.py
  ```

### **3. `update_to_static.py`**
- **Purpose**: Migrates existing product image paths from the legacy `/media/` folder to the new standardized `/static/products/` structure.

---

## 🚀 **Setup Instructions**

### **1. Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Database Setup**
```bash
python manage.py migrate
python seed_data.py  # Creates superuser (admin/admin123)
```

### **4. Run Server**
```bash
python manage.py runserver
```

---

## 📁 **Project Components**

- **`products/`**: Core catalog management (Categories, Products, Customization Zones).
- **`orders/`**: E-commerce logic (Cart, Orders, Addresses, Razorpay integration).
- **`inquiries/`**: B2B bulk inquiry handling with file attachment support.
- **`company_info/`**: Dynamic site content (Testimonials, Global Settings).
- **`core/`**: JWT configuration, CORS settings, and static/media handling.

---

## 🔐 **Admin Panels**

### **A. Django Admin**
- **URL**: `http://127.0.0.1:8000/admin`
- **Features**: Deep data management, inquiry review, and category control.

### **B. React Admin Dashboard**
- **URL**: `http://localhost:5173/admin-panel/`
- **Features**: Modern UI for quick order management and real-time dashboard stats.

---

## 📡 **Core API Endpoints**

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/products/` | `GET` | List products (supports `?category=`, `?search=`) |
| `/api/categories/` | `GET` | All active categories |
| `/api/bulk-inquiry/` | `POST` | Submit B2B inquiry (supports multipart logo/mockup) |
| `/api/auth/login/` | `POST` | JWT login |
| `/api/orders/create-order/` | `POST` | Place a new order |

---

## ⚠️ **Security & Standards**
- **CORS**: Configured via `django-cors-headers`. Update `CORS_ALLOWED_ORIGINS` for production.
- **JWT**: Tokens expire in 24 hours. Refresh tokens valid for 7 days.
- **Static Assets**: All product images are served from `/static/products/` for cross-platform filename stability.
