# Soham_Gift - Project Memory & Context

## 1. Tech Stack
- **Backend:** Python, Django, Django REST Framework
- **Frontend:** React (Vite)
- **Database:** SQLite/PostgreSQL (configured in `core/settings.py`)

## 2. Directory Structure & Key Paths
- **Backend:** `c:\Users\Asus\Downloads\New folder\Soham_Gift\backend`
- **Frontend:** `c:\Users\Asus\Downloads\New folder\Soham_Gift\frontend`
- **Product Images:** `backend/static/products/`
- **Frontend API Config:** `frontend/.env` (`VITE_API_BASE_URL=http://localhost:8000/api`)

## 3. Database Rules & Behaviors (Very Important)
- **Soft Deletions:** The `Product` model has an `is_deleted` boolean flag. Standard `Product.objects` only returns active products. To find hidden or soft-deleted products, ALWAYS use `Product.all_objects`.
- **Hard Deletions vs Soft Deletions:** Deleting a `Category` using Django's `.delete()` performs a hard cascade delete on all its products. 
- **Historical Records:** The `Product` model uses `simple_history`. If a product is accidentally deleted or modified, its previous state can be recovered using `Product.history`.

## 4. Past Issues & Bug Fixes
- **Image Mismatch Bug (Fixed):** Many products were not showing images on the frontend because their `image` CharField in the database didn't match the actual file name in `backend/static/products/`. We wrote a script (`fix_images.py`) to auto-match product names to their correct `.png`/`.jpg`/`.webp` files. Any new products added should have exact matching filenames.
- **Ghost Products Bug (Fixed):** Some products were still appearing after deletion because the API was hitting a different environment or they were only soft-deleted. Hard-deleting them via `Product.all_objects.filter(...).delete()` fixed it permanently.

## 5. Development Workflow
- Backend server runs on: `python manage.py runserver` (Port 8000)
- Frontend server runs on: `npm run dev` (Port 5173)

## 6. User Preferences & AI Rules
- **Daily Chat Logs:** Whenever the user types a message or discusses a task in the chat, the AI must summarize the "best version" (key takeaways, decisions, and important context) of that chat and append it to this `memory.md` file (like a daily chat upload/log). This ensures the memory file acts as an evolving diary of all important interactions.

## 7. Features & Implementations
- **File Uploads (Logo & Customizations):** 
  - The project supports multiple formats for printing and customizations: `.pdf`, `.ai`, `.psd`, `.cdr`, `.png`, `.jpeg`, `.jpg`, `.tiff`, `.tif`, and `.bmp`.
  - **Frontend Implementation:** `LogoUploader.jsx` actively validates and handles these files (size limits: 10MB per file, 100MB total) before submission.
  - **Backend Implementation:** The backend (`CartItemLogo` and `OrderItemLogo` in `orders/models.py`) uses Django's `FileField` (instead of `ImageField`), allowing it to seamlessly accept and store heavy vector/design files without image validation errors.
  - **UI/UX Note:** The "Upload Guidelines" section in `LogoUploader.jsx` has been converted into a collapsible dropdown to save screen space.
