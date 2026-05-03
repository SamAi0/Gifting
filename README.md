# **Soham Gift - Corporate Gifting Platform**

Soham Gift is a **premium full-stack B2B corporate gifting e-commerce platform**. It is designed to bridge the gap between browsing a catalog and visualizing custom brand placement on products in real-time.

---

## 🚀 **Core Features**

### 🎨 **Advanced Branding Engine (Live Customizer)**
The standout feature of the platform, powered by **Fabric.js**:
- **Real-time Visualization**: See your logo and text on products instantly.
- **Curved Text Support**: Dynamic wrapping for rounded surfaces (Mugs, Bottles).
- **Intelligent Auto-Fit**: Automatic font resizing and character spacing to ensure branding stays within boundaries.
- **Developer Mapping Mode**: Visual coordinate picking tool accessible via `?dev=true` or `?dev=1`.
- **High-Res Mockups**: Generates 2x resolution PNGs for production-ready inquiries.

### 📦 **E-Commerce & B2B Workflow**
- **Bulk Inquiries**: Specialized workflow for corporate clients to request quotes with mockups attached.
- **Direct Orders**: Full cart and checkout flow with Razorpay integration.
- **Responsive Design**: Premium, pixel-perfect UI/UX using Tailwind CSS and Framer Motion.
- **Dual Admin System**: Manage via modern React Dashboard or robust Django Admin.

---

## 🛠️ **Tech Stack**

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Django 4.2+, Django REST Framework, SQLite, JWT, Pillow |
| **Frontend** | React 19, Vite, Tailwind CSS, Fabric.js, Framer Motion, Axios |
| **Design** | Lucide Icons, Google Fonts (Outfit, Inter) |
| **Payments** | Razorpay (Test/Prod ready) |

---

## 📋 **Standard Operating Procedures (SOP)**

### **How to Add a New Customizable Product**

1. **Prepare Assets**:
   - Save the product base image in `backend/static/products/`.
   - Use `lowercase_with_underscores.png` naming convention.
2. **Mirror Assets**:
   - Copy the image to `frontend/public/static/products/` for frontend stability.
3. **Map Branding Zones**:
   - Open any product in the frontend with `?dev=true`.
   - Click on the image to find the `x` and `y` coordinates (0-1000 scale).
4. **Update Configuration**:
   - Add the product and its zones to `frontend/src/data/customization.json`.
5. **Sync Database**:
   ```bash
   cd backend
   python sync_customization.py  # Updates branding zones
   python seed_products.py       # Ensures image paths and product data match
   ```

---

## 🔧 **Recent Stabilization Fixes**

### ✅ **Canvas Engine Hardening**
- Resolved race conditions where `loadBaseImage` was called before the Fabric canvas initialized.
- Implemented robust async/await flow for canvas lifecycle management.

### ✅ **Image Resolution Standard**
- Standardized image URL resolution using a centralized `getImageUrl` utility.
- Migrated all product images to `/static/products/` to prevent 404s in production environments (like Netlify).
- Implemented lowercase/underscore naming enforcement to resolve case-sensitivity issues on Linux servers.

### ✅ **Admin & Data Integrity**
- Migrated synchronization logic to use persistent **slugs** instead of volatile IDs.
- Added comprehensive logging in the Django Admin to prevent 500 errors during media loading.

---

## 🚀 **Getting Started**

### **Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python seed_data.py          # Creates admin/admin123
python manage.py runserver
```

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 **Project Structure**

- `/frontend`: React application, assets, and branding data.
- `/backend`: Django API, product models, and inquiry management.
- `/frontend/src/data/customization.json`: The source of truth for all branding coordinates.

---

## ⚠️ **Known Constraints**

- **Image Naming**: Always use `lowercase_with_underscores.png`. Spaces or special characters in filenames will cause loading failures on production servers.
- **CORS**: Ensure your frontend URL is added to `CORS_ALLOWED_ORIGINS` in `backend/core/settings.py`.

---

## 🌟 **Current Status**
The platform is in **Stable Beta**. Core features including customization, cart, and checkout are fully functional. Production deployment requires migrating to a persistent database (PostgreSQL) and production Razorpay keys.