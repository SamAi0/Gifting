# Soham Gift - Backend (Django)

This is the backend API and management system for the Soham Gift corporate gifting platform.

## Setup Instructions

1. **Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   ```bash
   python manage.py migrate
   ```

4. **Seed Initial Data**:
   This script creates a superuser (`admin`/`admin123`) and initial categories.
   ```bash
   python seed_data.py
   ```

5. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Project Components

- **`core/`**: Project configuration and settings.
- **`api/`**: REST API implementation using Django REST Framework.
- **`products/`**: Product and Category models and logic.
- **`inquiries/`**: Handles bulk inquiry form submissions.
- **`company_info/`**: Manages dynamic site settings (Contact details, etc.).

## Admin Panel

Access the admin dashboard at `http://127.0.0.1:8000/admin`.
Manage your products, view inquiries, and update company contact information here.

## API Endpoints

- **GET `/api/products/`**: List all products (supports filtering).
- **GET `/api/products/<id>/`**: Get product details.
- **GET `/api/categories/`**: List all product categories.
- **GET `/api/settings/`**: Get company contact info and tagline.
- **POST `/api/bulk-inquiry/`**: Submit a new bulk inquiry (Multipart form for attachments).
- **POST `/api/contact/`**: General contact form submission.
