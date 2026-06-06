# **Soham Gift - Frontend (React)**

This is the high-performance React frontend for the Soham Gift platform. It features a premium design system and a sophisticated product branding engine.

---

## 🎨 **The Branding Engine (`CanvasCustomizer`)**

The core of this frontend is the **Live Branding Engine**, built on **Fabric.js**. It allows users to visualize their identity on physical products with high precision.

### **Key Technical Features**
- **Dynamic Coordinate System**: Branding zones are defined in a normalized `0-1000` coordinate system in `customization.json`, making them responsive to any canvas size.
- **Curved Text Implementation**: Uses a custom group-based rendering logic to wrap characters along a radius for rounded products.
- **Intelligent Auto-Fit**:
  - Monitors object width in real-time.
  - Automatically reduces `fontSize` down to a specified `minFontSize`.
  - Adjusts `charSpacing` if text still exceeds the `maxWidth`.
  - Provides visual warnings to the user when "Max Fit" is reached.
- **High-Resolution Exports**: Generates 2x multiplier PNGs for clear, production-ready mockups.

---

## 🛠️ **Developer Tools: Mapping Mode**

To make it easy to add new products, the frontend includes a **Developer Mapping Tool**.

### **How to Use Mapping Mode**
1. Navigate to any product detail page.
2. Add `?dev=true` to the URL (e.g., `/products/1?dev=true`).
3. **Click anywhere** on the product image.
4. Check the **Browser Console (`F12`)**.
5. The exact `x` and `y` coordinates in the `0-1000` scale will be logged, along with a ready-to-copy JSON snippet.

---

## 📁 **Asset Strategy & Stability**

### **Standardized Static Paths**
To prevent loading failures and 404 errors (especially on case-sensitive production servers):
- **Location**: All product base images must be stored in `public/static/products/`.
- **Naming**: Use `lowercase_with_underscores.png`.
- **Why?**: This ensures that images are served reliably by the frontend's static server (Vite/Netlify) and are decoupled from backend media volatility.

---

## 🚀 **Setup Instructions**

### **1. Install Dependencies**
```bash
npm install
```

### **2. Environment Variables**
Create a `.env` file in the `frontend/` root:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### **3. Start Development Server**
```bash
npm run dev
```

---

## 📦 **Available Scripts**

- `npm run dev`: Starts the Vite development server.
- `npm run build`: Generates the production bundle.
- `npm run lint`: Runs ESLint for code quality.
- `npm run preview`: Previews the production build locally.

---

## 🏗️ **Key Technologies**

- **React 19**: Modern UI library with Concurrent Mode support.
- **Vite 8**: Next-generation frontend tooling for fast builds.
- **Fabric.js 7**: Powerful HTML5 canvas library for the branding engine.
- **Tailwind CSS 4**: Utility-first styling for a premium look.
- **Framer Motion 12**: Industrial-strength animation for smooth interactions.
- **Lucide React**: Clean and consistent iconography.
