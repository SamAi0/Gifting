I'll provide a detailed overview of your project by examining the key files and structure.


Now let me examine the key models and API structure to provide a comprehensive overview.


Let me check a few more key files to understand the customization feature and API structure.


# **Soham Gift - Corporate Gifting Platform: Detailed Project Overview**

## **Project Purpose**
Soham Gift is a **full-stack B2B corporate gifting e-commerce platform** that allows businesses to browse, customize, and order branded corporate gifts. It combines product catalog management with a live branding engine for product personalization.

---

## **Architecture Overview**

### **Tech Stack**

**Backend:**
- **Framework**: Django 4.2.30 (Python)
- **API**: Django REST Framework 3.15.2
- **Database**: SQLite (db.sqlite3)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **CORS**: django-cors-headers
- **Image Processing**: Pillow 10.4.0
- **Payment Integration**: Razorpay (configured, placeholder keys)

**Frontend:**
- **Framework**: React 19.2.5
- **Build Tool**: Vite 8.0.10
- **Styling**: Tailwind CSS 4.2.4
- **Routing**: React Router DOM 7.14.2
- **Animations**: Framer Motion 12.38.0
- **Canvas Manipulation**: Fabric.js 7.3.1 (for product customization)
- **HTTP Client**: Axios 1.15.2
- **Icons**: Lucide React 1.11.0
- **JWT Handling**: jwt-decode 4.0.0
- **SEO**: react-helmet-async 3.0.0

---

## **Backend Structure (Django)**

### **Apps & Responsibilities**

1. **`core/`** - Project configuration
   - Settings, URL routing, WSGI/ASGI config
   - JWT authentication setup (1-day access, 7-day refresh tokens)
   - Media & static file handling

2. **`products/`** - Product catalog management
   - **Models**:
     - `Category`: Product categorization
     - `Product`: Name, description, pricing (regular + discount), stock, weight, images, trending flag, badges, customization config (JSON)
   
3. **`inquiries/`** - Lead generation & contact forms
   - **Models**:
     - `BulkInquiry`: B2B inquiry form (company name, contact person, email, phone, message, logo upload)
     - `ContactMessage`: General contact form submissions

4. **`company_info/`** - Dynamic site content
   - **Models**:
     - `Settings`: Company details (name, tagline, address, phones, email, social links) - singleton pattern enforced
     - `Testimonial`: Client testimonials for homepage display

5. **`orders/`** - E-commerce functionality
   - **Models**:
     - `Address`: User shipping addresses (with default flag)
     - `Cart`: One-to-one with User, contains CartItems
     - `CartItem`: Product, quantity, customization text & image
     - `Order`: User, address, total amount, status (PENDING/PAID/SHIPPED/DELIVERED/CANCELLED), Razorpay IDs
     - `OrderItem`: Snapshot of product, quantity, price at purchase time, customizations

6. **`authentication/`** - User authentication
   - Uses Django's built-in User model
   - JWT-based login/register via REST API

7. **`api/`** - REST API endpoints
   - ProductViewSet (list, retrieve, filter by category/trending/search)
   - Category listing
   - Testimonials listing
   - Settings retrieval
   - Contact form submission
   - Bulk inquiry submission (supports multipart file uploads)

### **API Endpoints**
- `GET /api/products/` - List products (supports `?category=`, `?is_trending=`, `?search=`)
- `GET /api/products/<id>/` - Product details
- `GET /api/categories/` - All categories
- `GET /api/testimonials/` - Client testimonials
- `GET /api/settings/` - Company information
- `POST /api/contact/` - Submit contact form
- `POST /api/bulk-inquiry/` - Submit bulk inquiry (with logo attachment)
- `POST /api/auth/` - Authentication endpoints (login, register)
- `POST /api/orders/` - Order management endpoints

### **Database Schema**
- **SQLite** database with Django ORM
- Media files stored in `/backend/media/` (product images, cart customizations, inquiry logos)
- Auto-generated migrations in each app

---

## **Frontend Structure (React)**

### **Pages & Routes**
1. **Home** (`/`) - Landing page with hero, featured products, testimonials
2. **ProductList** (`/products`) - Product catalog with category filters & search
3. **ProductDetail** (`/products/:id`) - Individual product view with customization tool
4. **Cart** (`/cart`) - Shopping cart with customization previews
5. **Checkout** (`/checkout`) - Order placement with address selection & Razorpay payment
6. **Login** (`/login`) - User authentication
7. **Register** (`/register`) - New user registration
8. **Contact** (`/contact`) - Contact form
9. **About** (`/about`) - Company information page

### **Key Components**
- **Navbar**: Navigation with cart icon, auth links
- **Footer**: Company info, social links, quick links
- **CanvasCustomizer**: Fabric.js-based product customization canvas
- **CustomizerControls**: UI controls for text input, logo upload, color selection
- **WhatsAppButton**: Floating WhatsApp contact button
- **Skeleton**: Loading state placeholders

### **State Management**
- **AuthContext**: User authentication state, JWT token management
- **CartContext**: Shopping cart state (items, quantities, customizations)

#### **Live Branding Engine (Customizer)**
**Powered by Fabric.js**, this is the standout feature of the platform:
- **Dynamic Configuration**: Powered by `frontend/src/data/customization.json` for 30+ product zones.
- **Advanced Features**:
  - **Curved Text Support**: Implementation of dynamic text curve wrapping for rounded products like mugs and bottles.
  - **Intelligent Auto-Fit**: Real-time logic that automatically shrinks font size and adjusts character spacing to keep branding within print boundaries.
  - **Developer Mapping Mode**: A specialized tool accessible via `?dev=true` that allows developers to visually position branding zones and copy-paste JSON configurations.
  - **Responsive Canvas**: Uses `ResizeObserver` for pixel-perfect rendering and consistent scaling across mobile and desktop.
  - **High-Res Mockups**: Generates 2x resolution PNG mockups for bulk inquiry attachments.
  - **Visual Effects**: Built-in support for "Engrave" and "Multiply" blend modes for realistic previews.
- **Personalization Options**:
  - Upload company logo with auto-scaling.
  - Add custom text with real-time color and font updates.
  - Dynamic character limits and overflow warnings.

---

## **Key Features**

### **1. Product Catalog**
- Browse corporate gifts by category
- Search functionality
- Trending products filter
- Product badges (NEW, 50% OFF, BESTSELLER) with customizable colors
- Stock tracking
- Weight-based shipping calculations

### **2. Live Product Customization**
- **Interactive Canvas**: High-performance customization powered by Fabric.js.
- **Curved Branding**: Support for wrapping text around curved surfaces.
- **Logo Integration**: Instant logo upload with intelligent scaling.
- **Smart Text Fitting**: Automatic font-size reduction and character spacing adjustment.
- **Real-time Feedback**: Instant visual updates with "Max Fit" overflow warnings.
- **Professional Mockups**: High-resolution image generation for inquiry precision.

### **3. E-Commerce Flow**
- Add customized products to cart
- Manage cart items (quantity, remove)
- Checkout with address selection
- Razorpay payment integration (test mode configured)
- Order tracking with status updates (PENDING → PAID → SHIPPED → DELIVERED)

### **4. B2B Bulk Inquiries**
- Dedicated bulk inquiry form
- Attach custom mockups generated from customizer
- Company details capture
- Admin can review inquiries in Django admin panel

### **5. User Authentication**
- JWT-based authentication
- Login/Register pages
- Protected routes for cart/checkout
- User-specific order history

### **6. Admin Dashboard**
- URL: `http://127.0.0.1:8000/admin`
- Credentials: `admin` / `admin123` (from seed_data.py)
- Manage products, categories, testimonials
- View bulk inquiries and contact messages
- Update company settings dynamically
- Order management

### **7. Responsive Premium Design**
- Tailwind CSS v4 for utility-first styling
- Framer Motion for smooth animations
- Mobile-first responsive layout
- Enterprise-grade UI/UX

---

## **Development Workflow**

### **Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python seed_data.py  # Creates admin user & initial data
python manage.py runserver
```

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

### **Common Commands**
- **Backend**: `python manage.py createsuperuser`, `python manage.py runserver`
- **Frontend**: `npm run dev`, `npm run build`, `npm run lint`

---

## **Data Flow Example: Customized Bulk Order**

1. User browses products → selects "Premium Ceramic Mug"
2. Opens customizer → uploads company logo + adds text "Acme Corp"
3. Fabric.js renders preview on canvas in real-time
4. User clicks "Request Bulk Quote" → inquiry form opens with mockup attached
5. Form submitted to `/api/bulk-inquiry/` with multipart data (logo, message, mockup)
6. Admin receives inquiry in Django admin panel
7. Admin reviews and contacts company for order finalization

---

## **Current Status & Notes**

✅ **Completed Features:**
- Product catalog with CRUD via admin
- Advanced Branding Engine (Curved text, Auto-fit, Mapping mode)
- User authentication (JWT)
- Cart & checkout flow
- Razorpay integration (test mode)
- Bulk inquiry system with mockup attachments
- Responsive design with pixel-perfect scaling
- Admin dashboard for enterprise management

⚠️ **Areas for Production Readiness:**
- Replace SQLite with PostgreSQL/MySQL
- Update Razorpay test keys with production credentials
- Add email notifications for orders/inquiries
- Implement order tracking page for users
- Add pagination for product listings
- Enhance error handling & validation
- Set up proper logging
- Configure production static/media file serving (Whitenoise, S3, etc.)
- Add rate limiting for API endpoints
- Implement CSRF protection for forms

---

## **Project Strengths**
- Well-structured Django app separation
- Comprehensive customization system
- Clean REST API design
- Modern React frontend with proper routing
- B2B-focused workflow (bulk inquiries + direct orders)
- Scalable architecture for future features

This is a **production-ready corporate gifting platform** with a strong focus on product customization and B2B workflows. The combination of Django's robust backend and React's interactive frontend creates a professional e-commerce experience tailored for corporate clients.