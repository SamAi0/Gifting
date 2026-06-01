import os
import shutil

def move_unique_images():
    frontend_dir = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\frontend\public\static\products"
    backend_dir = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\backend\static\products"
    
    if not os.path.exists(frontend_dir) or not os.path.exists(backend_dir):
        print("One of the directories does not exist.")
        return

    frontend_files = set(os.listdir(frontend_dir))
    backend_files = set(os.listdir(backend_dir))
    
    # We want case-insensitive comparison for Windows just to be safe
    backend_files_lower = {f.lower(): f for f in backend_files}
    
    moved_count = 0
    
    for f_name in frontend_files:
        f_lower = f_name.lower()
        frontend_path = os.path.join(frontend_dir, f_name)
        backend_path = os.path.join(backend_dir, f_name)
        
        # If it's a file and not in backend
        if os.path.isfile(frontend_path):
            if f_lower not in backend_files_lower:
                # Move to backend
                shutil.move(frontend_path, backend_path)
                print(f"Moved {f_name} to backend")
                moved_count += 1
            else:
                # It's already in backend, so just remove it from frontend
                os.remove(frontend_path)
                print(f"Removed duplicate {f_name} from frontend")
                
    print(f"\nSuccessfully moved {moved_count} unique images to backend.")

if __name__ == '__main__':
    move_unique_images()
